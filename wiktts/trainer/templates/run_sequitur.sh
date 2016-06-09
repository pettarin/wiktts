#!/bin/bash

# Generated by wiktts.trainer
# Version 0.1.0
# Date 2016-06-07

BASE="{BASE}"
TRAIN="{BASE}.train"
TEST="{BASE}.test"
WORDS="{BASE}.words"
TRAINWORDS="$TRAIN.words"
TESTWORDS="$TEST.words"

LOG="{BASE}.sequitur.log"
MODELPREFIX="{BASE}.model."
MAXORDER="{MAXORDER}"
DEVEL="{DEVEL}%"
VARIANTS="{VARIANTS}"

### NORMALLY YOU SHOULD NOT NEED TO EDIT BELOW THIS LINE

usage() {{
    echo ""
    echo "$ bash $0 train [ORDER [--only]]"
    echo "$ bash $0 test [ORDER]"
    echo "$ bash $0 apply FILE [ORDER] [VARIANTS]"
    echo "$ bash $0 clean"
    echo ""
    echo "Parameters:"
    echo "  maxorder: {MAXORDER}"  
    echo "  devel:    {DEVEL}%"
    echo "  variants: {VARIANTS}"
    echo ""
    exit 2
}}

run_train_order() {{
    START=`date +%s`
    L=$1
    M="$MODELPREFIX""$L"
    R=""
    if [ "$L" -gt 1 ]
    then
        P=$((L - 1))
        PREVM="$MODELPREFIX""$P"
        if [ ! -e "$PREVM" ]
        then
            echo "[ERROR] To train at order $L you need file $PREVM (i.e., train at order $P first)"
            exit 1
        fi
        R="--model $PREVM --ramp-up"
    fi
    echo "" >> $LOG
    echo "==============================" >> $LOG
    echo "Training model $L..." | tee -a $LOG
    echo "" >> $LOG
    g2p.py --enc "utf-8" --devel "$DEVEL" --train "$TRAIN" $R --write-model "$M" 2>> $LOG >> $LOG
    END=`date +%s`
    DIFF=`echo "$END - $START" | bc`
    echo "" >> $LOG
    echo "Training model $L... done in $DIFF s" | tee -a $LOG
    echo "==============================" >> $LOG
    echo "" >> $LOG
}}

run_test() {{
    L=$1
    M="$MODELPREFIX""$L"
    if [ ! -e "$M" ]
    then
        echo "[ERROR] To test at order $L you need file $M (i.e., train at order $L first)"
        exit 1
    fi
    g2p.py --enc "utf-8" --model "$M" --test "$TEST"
}}

run_apply() {{
    F=$1
    L=$2
    V=$3
    M="$MODELPREFIX""$L"
    if [ ! -e "$M" ]
    then
        echo "[ERROR] To apply at order $L you need file $M (i.e., train at order $L first)"
        exit 1
    fi
    C="$F.nospaces"
    A="$F.applied"
    sed -e 's/ //g' "$F" > "$C"
    echo "[INFO] Removed spaces, created file $C"
    ALOG="$A.log"
    if [ "$V" -gt 1 ]
    then
        g2p.py --enc "utf-8" --model "$M" --apply "$C" --variants-number "$V" > "$A" 2> "$ALOG"
    else
        g2p.py --enc "utf-8" --model "$M" --apply "$C" > "$A" 2> "$ALOG"
    fi
    echo "[INFO] Logged errors to file $ALOG"
    echo "[INFO] Created file $A"
}}

run_clean() {{
    rm -f $MODELPREFIX*
}}

if [ "$#" -lt 1 ]
then
    usage
fi
COMMAND=$1

if [ "$COMMAND" == "clean" ]
then
    run_clean
    exit 0
fi

if [ "$COMMAND" == "train" ]
then
    ORDER=$MAXORDER
    if [ "$#" -ge 2 ]
    then
        ORDER=$2
    fi
    
    rm -f $LOG
    ONLY=0
    if [ "$#" -ge 3 ] && [ "$3" == "--only" ]
    then
        ONLY=1
    fi
    if [ "$ONLY" -eq 1 ]
    then
        run_train_order $ORDER
    else
        for ((i=1; i <= ORDER; ++i))
        do
            run_train_order $i
        done
    fi
    exit 0
fi

if [ "$COMMAND" == "test" ]
then
    ORDER=$MAXORDER
    if [ "$#" -ge 2 ]
    then
        ORDER=$2
    fi
    
    run_test $ORDER
    exit 0
fi

if [ "$COMMAND" == "apply" ]
then
    if [ "$#" -lt 2 ]
    then
        usage
    fi
    FILE=$2

    ORDER=$MAXORDER
    if [ "$#" -ge 3 ]
    then
        ORDER=$3
    fi

    VAR=$VARIANTS
    if [ "$#" -ge 4 ]
    then
        VAR=$4
    fi

    run_apply $FILE $ORDER $VAR
    exit 0
fi

usage
