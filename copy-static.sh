#!/bin/bash
rm -r static
cd ..
cd front-demo
npm run build
cp -r ./build ../server/static