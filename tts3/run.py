import os
import argparse

root_dir = os.getcwd()
input_dir= root_dir + "/input/nahida"
input_all_dir= root_dir + "/input/all"  # 多说话人采用，懒得帮百度改代码
newdir_name="nahida_taw"
new_dir=input_dir + "/" + newdir_name
pretrained_model_dir= root_dir + "/pretrained_models/fastspeech2_aishell3_ckpt_1.1.0"
mfa_tools= root_dir + "/tools"
mfa_dir= root_dir + "/mfa_result"
dump_dir= root_dir + "/dump"
output_dir= root_dir + "/exp/default"
lang="zh"
ngpu=1
finetune_config= root_dir + "/conf/finetune.yaml"
replace_spkid=4

ckpt="snapshot_iter_117040"

gpus=1
stage=0

def run(stage):
    if stage == 0:
        check_oov()
    elif stage == 1:
        get_mfa_result()
    elif stage == 2:
        generate_duration()
    elif stage == 3:
        extract_feature()
    elif stage == 4:
        prepare_env()
    elif stage == 5:
        finetune()
    elif stage == 6:
        synthesize_e2e()


def exec_cmd(command):
    with os.popen(command, "r") as cmd:
        cmd_return = cmd.read()
        print(cmd_return)


def check_oov():
    print("check oov")
    command = "python local/check_oov.py --input_dir=%s --pretrained_model_dir=%s --newdir_name=%s --lang=%s" % (input_dir, pretrained_model_dir, newdir_name, lang)
    exec_cmd(command)


def get_mfa_result():
    print("get mfa result")
    command = "python3 local/get_mfa_result.py --input_dir=%s --mfa_dir=%s --lang=%s" % (new_dir, mfa_dir, lang)
    exec_cmd(command)


def generate_duration():
    print("generate duration")
    command = "python local/generate_duration.py --mfa_dir=%s" % mfa_dir
    exec_cmd(command)


def extract_feature():
    print("extract feature")
    command = "python local/extract_feature.py --duration_file=./durations.txt --input_dir=%s --dump_dir=%s --pretrained_model_dir=%s --replace_spkid=%d" % (new_dir, dump_dir, pretrained_model_dir, replace_spkid)
    exec_cmd(command)


def prepare_env():
    print("create finetune env")
    command = "python local/prepare_env.py --pretrained_model_dir=%s --output_dir=%s" % (pretrained_model_dir, output_dir)
    exec_cmd(command)


def finetune():
    print("finetune...")
    command = "python local/finetune.py --pretrained_model_dir=%s --dump_dir=%s --output_dir=%s --ngpu=%d --epoch=100 --finetune_config=%s" % (pretrained_model_dir, dump_dir, output_dir, ngpu, finetune_config)
    exec_cmd(command)


def synthesize_e2e():
    print("in hifigan syn_e2e")
    command = "python synthesize_e2e.py --am=fastspeech2_aishell3 --am_config=%s/default.yaml --am_ckpt=%s/checkpoints/%s.pdz \
             --am_stat=%s/speech_stats.npy --voc=hifigan_aishell3 --voc_config=pretrained_models/hifigan_aishell3_ckpt_0.2.0/default.yaml \
             --voc_ckpt=pretrained_models/hifigan_aishell3_ckpt_0.2.0/snapshot_iter_2500000.pdz --voc_stat=pretrained_models/hifigan_aishell3_ckpt_0.2.0/feats_stats.npy \
             --lang=%s --text=./sentences.txt --output_dir=./test_e2e/ --phones_dict=%s/phone_id_map.txt --speaker_dict=%s/speaker_id_map.txt \
             --spk_id=%d" % (pretrained_model_dir, output_dir, ckpt, pretrained_model_dir, lang, dump_dir, dump_dir, replace_spkid)
    exec_cmd(command)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, default=0)
    parser.add_argument('--stop-stage', type=int, default=0)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    start_stage = args.stage
    stop_stage = args.stop_stage
    if start_stage<=stop_stage:
        for i in range(start_stage, stop_stage+1):
            run(i)
    else:
        print("请输入正确的参数")


main()