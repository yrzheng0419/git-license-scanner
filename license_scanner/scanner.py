"""
scanner.py - 負責掃描資料夾尋找 LICENSE 檔案
"""

from pathlib import Path
from typing import List, Optional
from .licenses_db import LicenseDatabase

class LicenseScanner:
    """授權檔案掃描器"""
    
    # 常見的授權檔案名稱
    LICENSE_FILENAMES = [
        'LICENSE',
        'LICENSE.txt',
        'LICENSE.md',
        'COPYING',
        'COPYING.txt',
        'LICENSE-MIT',
        'LICENSE-APACHE',
    ]
    
    def __init__(self, root_path: str):
        """
        初始化掃描器
        
        Args:
            root_path: 要掃描的根目錄路徑
        """
        self.root_path = Path(root_path)
        self.license_db = LicenseDatabase()  # ← 新增這行
        
    def find_license_files(self) -> List[Path]:
        """
        尋找所有授權檔案
        
        Returns:
            找到的授權檔案路徑列表
        """
        found_files = []
        
        # 檢查根目錄是否存在
        if not self.root_path.exists():
            return found_files
        
        # 在根目錄尋找授權檔案
        for filename in self.LICENSE_FILENAMES:
            file_path = self.root_path / filename
            if file_path.exists() and file_path.is_file():
                found_files.append(file_path)
        
        return found_files
    
    def read_license_file(self, file_path: Path) -> Optional[str]:
        """
        讀取授權檔案內容
        
        Args:
            file_path: 授權檔案路徑
            
        Returns:
            檔案內容，如果讀取失敗則返回 None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"讀取檔案失敗: {e}")
            return None
    
    def scan(self) -> dict:
        """
        執行掃描
        
        Returns:
            掃描結果字典
        """
        license_files = self.find_license_files()
        
        results = {
            'path': str(self.root_path),
            'license_files': [],
            'summary': {  # ← 新增摘要資訊
                'total_files': 0,
                'identified': 0,
                'high_risk': 0,
                'medium_risk': 0,
                'low_risk': 0,
            }
        }
        
        for file_path in license_files:
            content = self.read_license_file(file_path)
            
            # ← 新增：識別授權類型
            identified_licenses = []
            if content:
                identified_licenses = self.license_db.identify_license(content)
            
            # ← 新增：更新統計
            results['summary']['total_files'] += 1
            if identified_licenses:
                results['summary']['identified'] += 1
                # 取最高信心度的授權
                top_license = identified_licenses[0]
                risk_level = top_license['risk_level']
                if risk_level == 'high':
                    results['summary']['high_risk'] += 1
                elif risk_level == 'medium':
                    results['summary']['medium_risk'] += 1
                else:
                    results['summary']['low_risk'] += 1
            
            # ← 修改：加入識別結果
            results['license_files'].append({
                'path': str(file_path),
                'name': file_path.name,
                'content': content,
                'size': file_path.stat().st_size,
                'identified_licenses': identified_licenses,  # ← 新增
            })
        
        return results


# 測試程式碼（更新版）
if __name__ == '__main__':
    # 測試掃描當前目錄
    scanner = LicenseScanner('.')
    results = scanner.scan()
    
    print(f"掃描路徑: {results['path']}")
    print(f"找到 {len(results['license_files'])} 個授權檔案\n")
    
    for file_info in results['license_files']:
        print(f"檔案: {file_info['name']}")
        print(f"大小: {file_info['size']} bytes")
        
        # ← 新增：顯示識別結果
        licenses = file_info['identified_licenses']
        if licenses:
            print(f"識別到的授權:")
            for lic in licenses:
                print(f"  - {lic['name']}: {lic['confidence']:.1f}% (risk level: {lic['risk_level']})")
        else:
            print(f"  無法識別授權類型")
        print()