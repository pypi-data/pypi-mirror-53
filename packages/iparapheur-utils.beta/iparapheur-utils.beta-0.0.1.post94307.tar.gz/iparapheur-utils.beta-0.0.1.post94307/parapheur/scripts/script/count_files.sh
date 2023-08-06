#!/bin/bash


PROP_PATH="/opt/iParapheur/tomcat/shared/classes/alfresco-global.properties"
PROP_PATH_MULTITENANT="/opt/iParapheur/tomcat/shared/classes/alfresco/extension/mt/mt-admin-context.xml"

if [ -f "$PROP_PATH" ]
then
  while IFS='=' read -r key value
  do
    key=$(echo $key | tr '.' '_')
    eval "${key}"=\${"value"} 2> /dev/null
  done < "$PROP_PATH"
else
  echo "- LE FICHIER DE PROPRIETE $1 EST INTROUVABLE : FIN DU SCRIPT"
  exit 1
fi


## -- Des variables
alfresco="/etc/init.d/alfresco"
PATH_IP="/opt/iParapheur/tomcat/shared/classes/"
db_url=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $1 }'`
db_port=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $2 }'`
DATA_PATH="$dir_root/contentstore/"
if [ -z "$db_port" ]
then
  db_port="3306"
fi
mysql="-h $db_url -P $db_port -u $db_username -p$db_password"

## -- Quelques test
IF_FILE_EXIST ()
{
if [ ! -f $1 ]; then
  echo "- LE DOSSIER $1 N'EXISTE PAS"
  echo " -FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


IF_DIR_EXIST ()
{
if [ ! -d $1 ]; then
  echo "LE DOSSIER $1 N'EXISE PAS"
  echo "- FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}

TEST_SERVICE ()
{
if ! which $1 >/dev/null; then
  echo "- LE SERVICE $1 N EXISTE PAS"
  echo "FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


## -- ON LANCE LES TESTS
echo -e "\n ** PREREQUIS **\n"
IF_FILE_EXIST $alfresco
IF_DIR_EXIST $PATH_IP
IF_FILE_EXIST $PROP_PATH
TEST_SERVICE "mysql"
IF_DIR_EXIST $DATA_PATH


mysql $mysql -e 'exit' $db_name
if [ $? -ne 0 ]; then
    echo "- CONNEXION A LA BASE DE DONNEES IMPOSSIBLE"
    echo "- FIN DU SCRIPT"
    exit 1
fi
echo -e "\n- CONNEXION A LA BASE DE DONNEES => OK\n"


## Procédures stockées
echo "DELIMITER //" > myproc.sql
echo "CREATE PROCEDURE count_files()" >> myproc.sql
echo "bEGIN" >> myproc.sql
echo "SELECT" >> myproc.sql
echo "  bureau.qname_localname AS Bureau_Name," >> myproc.sql
echo "  banette.qname_localname AS Bureau_Name," >> myproc.sql
echo "  COUNT(dossier.child_node_id) AS Dossiers_Count" >> myproc.sql
echo "FROM alf_child_assoc AS bureau" >> myproc.sql
echo "  JOIN alf_child_assoc AS banette ON bureau.child_node_id = banette.parent_node_id" >> myproc.sql
echo "          JOIN alf_child_assoc AS dossier ON dossier.parent_node_id = banette.child_node_id" >> myproc.sql
echo "WHERE bureau.parent_node_id = (" >> myproc.sql
echo "  SELECT child_node_id" >> myproc.sql
echo "  FROM alf_child_assoc" >> myproc.sql
echo "  WHERE child_node_name='parapheurs'" >> myproc.sql
echo "  LIMIT 1" >> myproc.sql
echo ")" >> myproc.sql
echo "AND banette.qname_localname IN ('retournes', 'a-archiver', 'a-traiter', 'en-preparation', 'en-retard', 'dossiers-delegues')" >> myproc.sql
echo "GROUP BY bureau.qname_localname, banette.qname_localname" >> myproc.sql
echo "HAVING Dossiers_Count >= 0;" >> myproc.sql
echo "END;" >> myproc.sql
echo "CREATE PROCEDURE count_files_by_tenant()" >> myproc.sql
echo "bEGIN" >> myproc.sql
echo "SELECT identifier, COUNT(*) " >> myproc.sql
echo "FROM alf_node_properties AS np, alf_node AS n, alf_store AS s " >> myproc.sql
echo "WHERE np.boolean_value=0 " >> myproc.sql
echo "AND np.qname_id=(SELECT id " >> myproc.sql
echo "FROM alf_qname AS q " >> myproc.sql
echo "WHERE q.ns_id=(SELECT ns.id " >> myproc.sql
echo "FROM alf_namespace AS ns " >> myproc.sql
echo "WHERE ns.uri='http://www.atolcd.com/alfresco/model/parapheur/1.0') " >> myproc.sql
echo "AND q.local_name='termine') " >> myproc.sql
echo "AND np.node_id=n.id " >> myproc.sql
echo "AND n.store_id=s.id " >> myproc.sql
echo "AND s.protocol='workspace' " >> myproc.sql
echo "AND n.node_deleted=0 " >> myproc.sql
echo "GROUP BY store_id;" >> myproc.sql
echo "END;" >> myproc.sql
echo "CREATE PROCEDURE count_files_archives_by_tenant()" >> myproc.sql
echo "bEGIN" >> myproc.sql
echo "SELECT identifier, COUNT(*) " >> myproc.sql
echo "FROM alf_node AS n, alf_qname AS q, alf_store AS s " >> myproc.sql
echo "WHERE n.type_qname_id=q.id " >> myproc.sql
echo "AND n.store_id=s.id " >> myproc.sql
echo "AND q.local_name='archive' " >> myproc.sql
echo "AND s.protocol='workspace' " >> myproc.sql
echo "AND n.node_deleted=0 GROUP BY store_id;" >> myproc.sql
echo "END;" >> myproc.sql
echo "//" >> myproc.sql
echo "DELIMITER ;" >> myproc.sql

## -- ON injecte la procédure
echo 'DROP PROCEDURE count_files'
mysql $mysql -e 'DROP PROCEDURE IF EXISTS count_files;' $db_name
echo 'DROP count_files_by_tenant'
mysql $mysql -e 'DROP PROCEDURE IF EXISTS count_files_by_tenant;' $db_name
echo 'DROP count_files_archives_by_tenant'
mysql $mysql -e 'DROP PROCEDURE IF EXISTS count_files_archives_by_tenant;' $db_name
echo 'CREATE PROCEDURE'
mysql $mysql $db_name < myproc.sql >/dev/null 2>&1


## -- On lance les procédures stockées selon que le parapheur est mono ou multitenant.
if [ -f "$PROP_PATH_MULTITENANT" ]
then
  echo "- PARAPHEUR MULTITENANT"
  mysql $mysql -e 'CALL count_files_by_tenant();' $db_name
  mysql $mysql -e 'CALL count_files_archives_by_tenant();' $db_name
  exit 1
else
  echo "- PARAPHEUR MONOTENANT"
  mysql $mysql -e 'CALL count_files();' $db_name
  exit 1
fi

exit 0

                                                                                                                               160,0-1       Bas
