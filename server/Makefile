.PHONY: all
all: go

get:
	git clone https://github.com/pjreddie/darknet.git ; \
	cd darknet ; \
	wget --no-cache -P . https://pjreddie.com/media/files/yolov2-tiny-voc.weights ; \
	wget --no-cache -P . https://firebasestorage.googleapis.com/v0/b/sciencefair-nk.appspot.com/o/dandelion-ready.zip?alt=media&token=8214aeaa-99a8-4fc5-aa70-953eec09fd76 ; \
	echo "Get complete!"

go:
	cd darknet; \
	unzip dandelion-ready.zip\?alt\=media ; \
	mv dandelion-ready dandelion ; \
	sed 's/GPU=0/GPU=1/g' Makefile ; \
	sed 's/CUDNN=0/CUDNN=1/g' Makefile
