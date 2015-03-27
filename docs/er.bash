#!/bin/bash
APPS="paloma"
MANAGE="../example/do.py"
GREP_OPTIONS=
echo  ${APPS}
for M in ${APPS} ; do
    echo ".. digraph:: ${M}" > source/${M}_models.dot ;
    echo ".. digraph:: ${M}" > source/${M}_models_no_members.dot ;
    echo "" >> source/${M}_models.dot ;
    echo "" >> source/${M}_models_no_members.dot ;
    $MANAGE graph_models ${M}| grep "^ " >> source/${M}_models.dot;
    $MANAGE graph_models -d ${M}| grep "^ " >> source/${M}_models_no_members.dot;

    $MANAGE db list_models ${M} --format=sphinx  >> source/models.rst
done
