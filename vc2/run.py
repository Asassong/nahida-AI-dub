import os
import argparse

root_dir = os.getcwd()
input_dir= root_dir + "/datasets/data_aishell3/train/wav"
mfa_dir= root_dir + "/mfa_result"
spk_emb_dir = root_dir + "/dump/embed"
conf_path=root_dir  + "/conf/default.yaml"
dump_dir= root_dir + "/dump"
train_output_path= root_dir + "/exp/default"
# pretrained_model = root_dir + "fastspeech2_aishell3_ckpt_vc2_1.2.0"  用预训练模型会出错
pretrained_model_dir= root_dir + "/pretrained_models/pwg_aishell3_ckpt_0.5"
ckpt_name = "snapshot_iter_5310"
text = "知识，与你分享！"
ref_audio_dir = root_dir + "/ref_audio"
ncpu = 4
ngpu = 1


def exec_cmd(command):
    with os.popen(command, "r") as cmd:
        cmd_return = cmd.read()
        print(cmd_return)


def pre_process(stage):
    if stage == 0:
        vc2_infer()
    elif stage == 1:
        get_mfa_result()
    elif stage == 2:
        extract_feature()
    elif stage == 3:
        compute_statistics()
    elif stage == 4:
        normalize()


def vc2_infer():
    command = "python fastspeech2/vc2_infer.py --input=%s --output=%s --num-cpu=%d" % (input_dir, spk_emb_dir, ncpu)
    exec_cmd(command)


def get_mfa_result():
    print("Generate durations.txt from MFA results ...")
    command = "python3 /utils/gen_duration_from_textgrid.py --inputdir=%s --output durations.txt --config=%s" % (mfa_dir, conf_path)
    exec_cmd(command)


def extract_feature():
    print("Extract features ...")
    command = "python fastspeech2/preprocess.py --dataset=aishell3 --rootdir=%s/datasets/data_aishell3/ --dumpdir=%s --dur-file=durations.txt --config=%s --num-cpu=%d --cut-sil=True \
    --spk_emb_dir=%s" % (root_dir, dump_dir, conf_path, ncpu, spk_emb_dir)
    exec_cmd(command)


def compute_statistics():
    print("Get features' stats ...")
    command = "python ./utils/compute_statistics.py --metadata=%s/dump/train/raw/metadata.jsonl --field-name=speech" % root_dir
    exec_cmd(command)
    command = "python ./utils/compute_statistics.py --metadata=%s/dump/train/raw/metadata.jsonl --field-name=pitch" % root_dir
    exec_cmd(command)
    command = "python ./utils/compute_statistics.py --metadata=%s/dump/train/raw/metadata.jsonl --field-name=energy" % root_dir
    exec_cmd(command)


def normalize():
    print("Normalize ...")
    command = "python fastspeech2/normalize.py --metadata=%s/dump/train/raw/metadata.jsonl --dumpdir=%s/dump/train/norm --speech-stats=%s/dump/train/speech_stats.npy \
    --pitch-stats=%s/dump/train/pitch_stats.npy --energy-stats=%s/dump/train/energy_stats.npy --phones-dict=%s/dump/phone_id_map.txt \
    --speaker-dict=%s/dump/speaker_id_map.txt" % (root_dir, root_dir, root_dir, root_dir, root_dir, root_dir, root_dir)
    exec_cmd(command)
    command = "python fastspeech2/normalize.py --metadata=%s/dump/dev/raw/metadata.jsonl --dumpdir=%s/dump/dev/norm --speech-stats=%s/dump/train/speech_stats.npy \
    --pitch-stats=%s/dump/train/pitch_stats.npy --energy-stats=%s/dump/train/energy_stats.npy --phones-dict=%s/dump/phone_id_map.txt \
    --speaker-dict=%s/dump/speaker_id_map.txt" % (root_dir, root_dir, root_dir, root_dir, root_dir, root_dir, root_dir)
    exec_cmd(command)
    command = "python fastspeech2/normalize.py --metadata=%s/dump/test/raw/metadata.jsonl --dumpdir=%s/dump/test/norm --speech-stats=%s/dump/train/speech_stats.npy \
    --pitch-stats=%s/dump/train/pitch_stats.npy --energy-stats=%s/dump/train/energy_stats.npy --phones-dict=%s/dump/phone_id_map.txt \
    --speaker-dict=%s/dump/speaker_id_map.txt" % (root_dir, root_dir, root_dir, root_dir, root_dir, root_dir, root_dir)
    exec_cmd(command)


# def prepare_env():
#     print("create finetune env")
#     command = "python local/prepare_env.py --pretrained_model_dir=%s --output_dir=%s" % (pretrained_model, train_output_path)
#     exec_cmd(command)


def train():
    # 不加speaker-dict，data_table.py报错，我没看到有这个参数为None的处理逻辑
    command = "python fastspeech2/train.py --train-metadata=%s/dump/train/norm/metadata.jsonl --dev-metadata=%s/dump/dev/norm/metadata.jsonl --config=%s \
    --output-dir=%s --ngpu=%d --phones-dict=%s/dump/phone_id_map.txt --speaker-dict=%s/dump/speaker_id_map.txt --voice-cloning=True" \
    % (root_dir, root_dir, conf_path, train_output_path, ngpu, root_dir, root_dir)
    exec_cmd(command)


def synthesize():
    command = "python synthesize.py --am=fastspeech2_aishell3 --am_config=%s --am_ckpt=%s/checkpoints/%s.pdz \
             --am_stat=%s/train/speech_stats.npy --voc=pwgan_aishell3 --voc_config=%s/default.yaml \
             --voc_ckpt=%s/snapshot_iter_1000000.pdz --voc_stat=%s/feats_stats.npy --test_metadata=%s/dump/test/norm/metadata.jsonl \
             --output_dir=%s/test --phones_dict=%s/phone_id_map.txt --speaker_dict=%s/speaker_id_map.txt \
             --voice-cloning=True" % (conf_path, train_output_path, ckpt_name, dump_dir,pretrained_model_dir,pretrained_model_dir, \
             pretrained_model_dir, root_dir, train_output_path, dump_dir, dump_dir)
    exec_cmd(command)


def voice_cloning():
    command = "python voice_cloning.py --am=fastspeech2_aishell3 --am_config=%s --am_ckpt=%s/checkpoints/%s.pdz \
             --am_stat=%s/train/speech_stats.npy --voc=pwgan_aishell3 --voc_config=%s/default.yaml \
             --voc_ckpt=%s/snapshot_iter_1000000.pdz --voc_stat=%s/feats_stats.npy --text=%s --input-dir=%s --output-dir=%s/vc_syn \
             --phones-dict=%s/phone_id_map.txt --use_ecapa=True" % (conf_path, train_output_path, ckpt_name, dump_dir,pretrained_model_dir, \
             pretrained_model_dir, pretrained_model_dir, text, ref_audio_dir, train_output_path, dump_dir)
    exec_cmd(command)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, default=0)
    parser.add_argument('--stop-stage', type=int, default=0)
    parser.add_argument('--purpose', type=int, default=0)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    start_stage = args.stage
    stop_stage = args.stop_stage
    purpose = args.purpose
    if purpose == 0:
        if start_stage<=stop_stage:
            for i in range(start_stage, stop_stage+1):
                pre_process(i)
        else:
            print("请输入正确的参数")
    elif purpose == 1:
        # if start_stage == 1:
        #     prepare_env()
        # else:
        train()
    elif purpose == 2:
        synthesize()
    elif purpose == 3:
        voice_cloning()

main()