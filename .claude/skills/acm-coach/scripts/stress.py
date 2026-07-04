#!/usr/bin/env python3
"""
ACM 对拍脚本 (Stress Test)
用法: python3 stress.py --sol ./solution --brute ./brute --gen ./gen [--limit 50]

只跑典型用例，不跑海量随机。发现差异时立即停止并保存失败用例。
不产生任何中间文件 —— 所有测试在内存中完成，只在失败时写一个 fail_input.txt。
"""

import subprocess, sys, os, argparse, time, atexit

FAIL_FILE = "fail_input.txt"

def cleanup():
    """确保没有残留临时文件"""
    for f in ["input.txt", "output.txt", "expected.txt"]:
        if os.path.exists(f): os.remove(f)

atexit.register(cleanup)

def run(exe, input_data, timeout):
    try:
        p = subprocess.run(
            [exe], input=input_data, capture_output=True, text=True,
            timeout=timeout, cwd=os.path.dirname(os.path.abspath(exe))
        )
        return p.stdout.strip(), p.stderr.strip(), p.returncode
    except subprocess.TimeoutExpired:
        return None, None, -1
    except FileNotFoundError:
        print(f"错误: 找不到可执行文件 '{exe}'，请先编译")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="ACM 对拍脚本（内存运行，无临时文件）")
    parser.add_argument("--sol", required=True, help="你的 solution")
    parser.add_argument("--brute", required=True, help="暴力正确解法")
    parser.add_argument("--gen", required=True, help="随机数据生成器")
    parser.add_argument("--timeout", type=float, default=2.0, help="单次超时(秒)")
    parser.add_argument("--limit", type=int, default=50, help="最大测试次数（默认 50，够用）")
    parser.add_argument("--verbose", action="store_true", help="显示每次测试")
    args = parser.parse_args()

    print(f"对拍: --sol {args.sol}  --brute {args.brute}  --gen {args.gen}")
    print(f"上限 {args.limit} 次  超时 {args.timeout}s")
    print("-" * 50)

    ok = 0
    t_start = time.time()
    for i in range(1, args.limit + 1):
        gen_result = run(args.gen, "", args.timeout)
        if gen_result[2] != 0:
            print(f"#{i}: 生成器崩溃 (exit={gen_result[2]})，跳过")
            continue
        input_data = gen_result[0]

        t0 = time.time()
        sol_out, sol_err, sol_rc = run(args.sol, input_data, args.timeout)
        sol_time = time.time() - t0
        brute_out, _, _ = run(args.brute, input_data, args.timeout * 5)

        if sol_rc == -1:
            print(f"#{i}: TLE ({args.timeout}s) — 检查死循环或复杂度")
            with open(FAIL_FILE, "w") as f: f.write(input_data)
            print(f"失败输入 → {FAIL_FILE}")
            break

        if sol_rc != 0:
            print(f"#{i}: RE (exit={sol_rc})")
            if sol_err: print(f"stderr: {sol_err[:200]}")
            with open(FAIL_FILE, "w") as f: f.write(input_data)
            print(f"失败输入 → {FAIL_FILE}")
            break

        if sol_out != brute_out:
            print(f"#{i}: WA — 输出不一致!")
            print(f"--- sol ({sol_time*1000:.0f}ms) ---\n{sol_out[:500]}")
            print(f"--- brute ---\n{brute_out[:500]}")
            with open(FAIL_FILE, "w") as f: f.write(input_data)
            print(f"失败输入 → {FAIL_FILE}")
            break

        ok += 1
        if args.verbose:
            print(f"#{i}: OK ({sol_time*1000:.0f}ms)")

    else:
        elapsed = time.time() - t_start
        print(f"通过 {ok} 次 ✅  ({elapsed:.1f}s, avg {elapsed/ok*1000:.0f}ms/test)")

if __name__ == "__main__":
    main()
