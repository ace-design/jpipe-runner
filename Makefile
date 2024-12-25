DIST_DIR = dist
BUILD_DIR = build
EGG_DIR = *.egg-info

all:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR) $(EGG_DIR)
