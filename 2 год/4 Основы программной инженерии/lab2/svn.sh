#!/bin/bash

set -e

ROOT="/c/Users/username/Desktop/Opi/lab2"
COMMITS="$ROOT/commits"
REPO_DIR="$ROOT/svnrepo"
WC="$ROOT/svnsrc"
REPO_URL="file:///$(cygpath -m "$REPO_DIR")"

echo "### Подготовка SVN ###"
rm -rf "$REPO_DIR" "$WC"

svnadmin create "$REPO_DIR"
svn mkdir "$REPO_URL/trunk" "$REPO_URL/branches" -m "create repo structure" --username red
svn checkout "$REPO_URL/trunk" "$WC"

cd "$WC"

echo "#############r0############"
cp -r "$COMMITS/commit0/." .
svn add * 
svn commit -m "r0" --username red

echo "#############r1############"
svn rm * 
cp -r "$COMMITS/commit1/." .
svn add * 
svn commit -m "r1" --username red

echo "#############r2############"
svn rm * 
cp -r "$COMMITS/commit2/." .
svn add * 
svn commit -m "r2" --username red

echo "#############r3############"
svn rm * 
cp -r "$COMMITS/commit3/." .
svn add * 
svn commit -m "r3" --username red

echo "#############r4############"
svn rm * 
cp -r "$COMMITS/commit4/." .
svn add * 
svn commit -m "r4" --username red

echo "#############r5############"
svn rm * 
cp -r "$COMMITS/commit5/." .
svn add * 
svn commit -m "r5" --username red

echo "### Создание blue-top ветки ###"
svn copy "$REPO_URL/trunk" "$REPO_URL/branches/blue-top" -m "create blue-top from r5" --username blue
svn switch "$REPO_URL/branches/blue-top" --username blue

echo "#############r6############"
svn rm * 
cp -r "$COMMITS/commit6/." .
svn add * 
svn commit -m "r6" --username blue

echo "### Создание blue-bottom ветки ###"
svn copy "$REPO_URL/branches/blue-top" "$REPO_URL/branches/blue-bottom" -m "create blue-bottom from r6" --username blue
svn switch "$REPO_URL/branches/blue-bottom" --username blue

echo "#############r7############"
svn rm * 
cp -r "$COMMITS/commit7/." .
svn add * 
svn commit -m "r7" --username blue

echo "### Переход к blue-top ###"
svn switch "$REPO_URL/branches/blue-top" --username blue

echo "#############r8############"
svn rm * 
cp -r "$COMMITS/commit8/." .
svn add * 
svn commit -m "r8" --username blue

echo "### Переход к trunk ###"
svn switch "$REPO_URL/trunk" --username red

echo "#############r9############"
svn rm * 
cp -r "$COMMITS/commit9/." .
svn add * 
svn commit -m "r9" --username red

echo "### Переход к blue-top ###"
svn switch "$REPO_URL/branches/blue-top" --username blue

echo "#############r10############"
svn rm * 
cp -r "$COMMITS/commit10/." .
svn add * 
svn commit -m "r10" --username blue

echo "### Переход к blue-bottom ###"
svn switch "$REPO_URL/branches/blue-bottom" --username blue

echo "#############r11############"
svn rm * 
cp -r "$COMMITS/commit11/." .
svn add * 
svn commit -m "r11" --username blue

echo "#############r12############"
svn switch "$REPO_URL/branches/blue-top" --username blue
svn update --username blue
svn merge "$REPO_URL/branches/blue-bottom" --accept postpone --username blue || true
svn rm * 
cp -r "$COMMITS/commit12/." .
svn add * 
svn status | awk '/^C/ {print $2}' | xargs -r svn resolve --accept working
svn commit -m "r12" --username blue

echo "#############r13############"
svn switch "$REPO_URL/trunk" --username red
svn update --username red
svn merge "$REPO_URL/branches/blue-top" --accept postpone --username red || true
svn rm * 
cp -r "$COMMITS/commit13/." .
svn add * 
svn status | awk '/^C/ {print $2}' | xargs -r svn resolve --accept working
svn commit -m "r13" --username red

echo "#############r14############"
svn rm * 
cp -r "$COMMITS/commit14/." .
svn add * 
svn commit -m "r14" --username red

echo "######### trunk #########"
svn log "$REPO_URL/trunk"

echo "######### blue-top #########"
svn log "$REPO_URL/branches/blue-top" --stop-on-copy

echo "######### blue-bottom #########"
svn log "$REPO_URL/branches/blue-bottom" --stop-on-copy