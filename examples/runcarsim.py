""" sample script to handle carsim solver """
from pycarsimlib import Vehicle
from datetime import timedelta

# declare params 
onestep_delta_time = timedelta(seconds=0.01)
total_sim_time = timedelta(minutes=1)
total_sim_step = total_sim_time / onestep_delta_time

# construct environment
env = Vehicle(simfile_path="C:\Users\Public\Documents\CarSim2022.1_Data\simfile.sim")

# reset environment
# observation, info = env.reset(オプショナルで初期状態の辞書型オブジェクト？)

try:
    # simulation loop
    for _ in range(10):

        # action = アクセルやブレーキなど, 辞書型オブジェクトで制御入力を指定
        # observation, terminated, info = env.step(action, delta_time=onestep_delta_time)
        # obsevation : 辞書型オブジェクト.
        # terminated : boolean, Trueならシミュレーション終了, Falseならシミュレーション続行.
        # info : エラーメッセージなどをテキストで取得.

        # print(observation) # 辞書型で取得
        # env.render() # carvizみたいなライブラリを他に作成して, observationの値を渡す方が疎結合になって良い.
        # carviz2dへ渡す情報は, (必須)グローバル車両位置・姿勢, (Optional) XY可視化範囲, 操舵角, trajectory

        # check flag for simulation termination
        if terminated:
            break

except KeyboardInterrupt:
    # catch Ctrl+C interruption
    pass

# terminate environment normally
env.close()