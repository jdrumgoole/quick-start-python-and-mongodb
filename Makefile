#
#
#
MONGODBBIN=`which mongod | xargs dirname 2>/dev/null`
REPLICASET_NAME="PYMM"
init_server:
	@echo "Setting up replica set";\
	if [ -d "data" ];then\
		echo "Replica set Already configured in 'data' start with make start_server";\
	else\
		echo "Making new mlaunch environment in 'data'";\
		pipenv run mlaunch init --binarypath ${MONGODBBIN} --replicaset --name ${REPLICASET_NAME};\
	fi

start_server:
	@echo "Starting MongoDB replica set"
	-@if [ -d "data" ];then\
		pipenv run mlaunch start;\
	else\
		echo "No mlaunch data, run make init_server";\
	fi

stop_server:
	@echo "Stopping MongoDB replica set"
	@if [ -d "data" ];then\
		pipenv run mlaunch stop;\
	else\
		echo "No mlaunch data, run make init_server";\
	fi

clean:
	rm -rf data

get_zip_data:
	mongodump --host demodata-shard-0/demodata-shard-00-00-rgl39.mongodb.net:27017,demodata-shard-00-01-rgl39.mongodb.net:27017,demodata-shard-00-02-rgl39.mongodb.net:27017 --ssl --username readonly --password readonly --authenticationDatabase admin --db demo --collection zipcodes

install_zip_data:
	mongorestore --drop
