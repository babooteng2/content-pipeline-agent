import glob
import os
import shutil
import tempfile
import time
import webbrowser


# flow.plot() 대체
# window유저의 임시 폴더에 생기더라도, 즉시 현재 프로젝트 폴더로 가져와서 권한 문제 없이 실행하게 함
def sync_and_cleanup_flow(flow_instance, folder_name="crewai_flow_chart"):
    # 1. CrewAI plot 실행 (임시 폴더에 생성됨)
    flow_instance.plot()

    # 2. 임시 폴더에서 'crewai_flow_*' 패턴의 가장 최근 폴더 찾기
    temp_root = tempfile.gettempdir()
    flow_dirs = glob.glob(os.path.join(temp_root, "crewai_flow_*"))

    if not flow_dirs:
        print("❌ 생성된 임시 폴더를 찾을 수 없습니다.")
        return

    # 가장 최근에 수정된 폴더 선택
    src_dir = max(flow_dirs, key=os.path.getmtime)

    # 3. 프로젝트 폴더 내 목적지 경로 설정
    dst_dir = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)

    try:
        # 4. 폴더 전체 복사 (HTML, JS, CSS 포함)
        shutil.copytree(src_dir, dst_dir)
        print(f"✅ 프로젝트 폴더로 복사 완료: {src_dir} >>> {dst_dir}")

        # 5. 복사 성공 후 AppData 내 원본 임시 폴더 삭제
        # (간혹 시스템이 파일을 점유 중일 수 있어 잠시 대기 후 삭제)
        time.sleep(1)
        shutil.rmtree(src_dir)
        print(f"🧹 임시 폴더 삭제 완료: {src_dir}")

        # 6. 복사된 로컬 파일 실행
        html_files = glob.glob(os.path.join(dst_dir, "*.html"))
        if html_files:
            webbrowser.open(f"file:///{html_files[0].replace('\\', '/')}")
        else:
            print("❌ 복사된 폴더 내에 HTML 파일이 없습니다.")

    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")
