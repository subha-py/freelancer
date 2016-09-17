#!/usr/bin/env bash
alias ci='inv ci'
alias runserver='python manage.py runserver'
alias pp='per_project'

function go() {
    for BASE in ~/PycharmProjects \
        ~/PycharmProjects/book/lino_book/projects
    do
      if [ -d $BASE/$1 ]
      then
        cd $BASE/$1;
        return;
      fi
    done
    echo Oops: no project $1
    return -1
}

function active() {
    for BASE in ~/PycharmProjects \
        ~/PycharmProjects/book/lino_book/projects
    do
      if [ -d $BASE/$1 ]
      then
        source ~/PycharmProjects/virtualenvs/$1_virtualenv/bin/activate
        return;
      fi
    done
    echo Oops: no project $1
    return -1
}