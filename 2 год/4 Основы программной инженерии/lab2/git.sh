#!/bin/bash

set -e

COMMITS="/c/Users/username/Desktop/Opi/lab2/commits"
WORK="/c/Users/username/Desktop/Opi/lab2/src"

echo "### Подготовка рабочей папки ###"
mkdir -p "$WORK"
cd "$WORK"

rm -rf .git
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

git init -b main
git config core.autocrlf false

git config user.name "red_user"
git config user.email "red_user@example.com"

echo "#############r0############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit0/." .
git add -A
git commit -m "r0"

echo "#############r1############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit1/." .
git add -A
git commit -m "r1"

echo "#############r2############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit2/." .
git add -A
git commit -m "r2"

echo "#############r3############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit3/." .
git add -A
git commit -m "r3"

echo "#############r4############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit4/." .
git add -A
git commit -m "r4"

echo "#############r5############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit5/." .
git add -A
git commit -m "r5"

echo "### Создание blue-top ветки ###"
git checkout -b blue-top
git config user.name "blue_user"
git config user.email "blue_user@example.com"

echo "#############r6############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit6/." .
git add -A
git commit -m "r6"

echo "### Создание blue-bottom ветки ###"
git checkout -b blue-bottom

echo "#############r7############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit7/." .
git add -A
git commit --allow-empty -m "r7"

echo "### Переход к blue-top ###"
git checkout blue-top

echo "#############r8############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit8/." .
git add -A
git commit -m "r8"

echo "### Переход к main ###"
git checkout main
git config user.name "red_user"
git config user.email "red_user@example.com"

echo "#############r9############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit9/." .
git add -A
git commit -m "r9"

echo "### Переход к blue-top ###"
git checkout blue-top
git config user.name "blue_user"
git config user.email "blue_user@example.com"

echo "#############r10############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit10/." .
git add -A
git commit -m "r10"

echo "### Переход к blue-bottom ###"
git checkout blue-bottom

echo "#############r11############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit11/." .
git add -A
git commit -m "r11"

echo "#############r12############"
git checkout blue-top
git merge --no-ff --no-commit blue-bottom || true
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit12/." .
git add -A
git commit -m "r12"

echo "#############r13############"
git checkout main
git config user.name "red_user"
git config user.email "red_user@example.com"
git merge --no-ff --no-commit blue-top || true
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit13/." .
git add -A
git commit -m "r13"

echo "#############r14############"
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -r "$COMMITS/commit14/." .
git add -A
git commit -m "r14"

echo "######### Вывод графа #########"
git log --graph --oneline --all --decorate