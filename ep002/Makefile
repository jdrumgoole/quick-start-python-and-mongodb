MONGODBBIN=`which mongod | xargs dirname 2>/dev/null`
PIDFILEPATH=`pwd`/mongod.pid
PIPBIN=`which pip 2>/dev/null`

start_server: mongod_check
	@echo "Starting MongoDB server"
	@if [ ! -d data ];then\
		mkdir data;\
	fi;\
	mongod --pidfilepath ${PIDFILEPATH} --dbpath data

stop_server: mongod_check
	@echo "Stopping MongoDB Server"
	@if [ -f ${PIDFILEPATH} ];then\
		cat ${PIDFILEPATH} | xargs kill;\
		rm ${PIDFILEPATH};\
	fi;\


mongod_check:
	@echo "Checking that mongod is on the path"
	@if [ "${MONGODBBIN}" = "" ];then\
	    echo "'mongod' is not on the path [MONGODBBIN is '' in the Makefile]";\
	    exit 1;\
	else\
	    echo "found mongod in ${MONGODBBIN}";\
	fi
clean:
	rm -rf data

python_shell: virtualenv
	@. venv/bin/activate && python

pip_check:
	@echo "Checking that pip is installed"
	@if [ "${PIPBIN}" = "" ];then\
		echo "pip is not installed. Please install using instructions from:";\
		echo "https://pip.pypa.io/en/stable/installing/";\
		${PYTHON} -m webbrowser "https://pip.pypa.io/en/stable/installing/";\
		exit 1;\
	fi

virtualenv: pip_check
	@pip install virtualenv
	@if [ ! -d "venv" ];then\
		echo "making virtualenv in 'venv'";\
		virtualenv -p python3 venv;\
	fi

pip_reqs: pip_check virtualenv
	@echo "Installing required python tools and packages"
	@. venv/bin/activate && pip install -r requirements.txt

