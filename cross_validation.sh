#これだとどう分割してるかわからなくて比較しづらい
#classias-train -tb -a pegasos.hinge -g5 -x features.txt


# split
# features.txt を split

#for 分割回数
for i in (seq 0 9)
do
    mv splits/split.$i tests/test.$i
    cat splits/* > trains/train.$i
    cp tests/test.$i splits/split.$i

    # train
    # classias-train -tb -a pegasos.hinge -m models/model.$i trains/train.$i
    # classias-train -tb -a pegasos.hinge -m models/distant.$i trains/distant.$i

    # test
    # cat tests/test.$i | classias-tag -m models/model.$i -t -r > evals/eval.$i
    # cat tests/test.$i | classias-tag -m models/distant.$i -t -r > evals/distant.$i

done

