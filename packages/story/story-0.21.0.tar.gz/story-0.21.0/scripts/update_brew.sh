#!/bin/bash

set -e
#set -x

pip=pip3.7
python=python3.7

tag=$1

if [ $tag == '' ]; then
    echo "Usage:"
    echo "bash update_brew.sh <tag>"
    exit 1
fi

echo "Retrieving git SHA for tag $tag..."
sha=`curl --silent https://api.github.com/repos/storyscript/cli/git/trees/$tag | $python -c "import sys, json; print(json.load(sys.stdin)['sha'])"`

BUILD_DIR=`mktemp -d`

echo "Building in $BUILD_DIR..."

cd $BUILD_DIR
echo "Creating a virtualenv..."
virtualenv --python=$python . &> /dev/null
source ./bin/activate
echo "Installing story==$tag..."
$pip install story==$tag &> /dev/null

echo "Cloning storyscript/homebrew-brew..."
git clone git@github.com:storyscript/homebrew-brew.git &> /dev/null
cd homebrew-brew

echo "Running pip freeze and building Formula/story.rb..."
$pip freeze | grep -v story== | $python scripts/build.py $tag $sha > Formula/story.rb
deactivate

echo "Updating brew..."
brew update
echo "Testing the formula locally with brew..."
brew install Formula/story.rb
story --version | grep $tag
story --help
git commit -a -m "Release $tag."
git tag $tag
git push origin master
git push origin master --tags

echo "Released!"

cd ../..
echo "Cleaning $BUILD_DIR..."
rm -rf $BUILD_DIR
echo "Done!"
