"""
licenses_db.py - 授權資料庫
包含各種開源授權的識別規則和資訊
"""

import re
from typing import Dict, List

class LicenseDatabase:
    """授權資料庫"""
    
    # 授權資料：名稱、模式、風險等級、說明
    LICENSES = [
        {
            'id': 'MIT',
            'name': 'MIT License',
            'patterns': [
                r'MIT\s+License',
                r'Permission is hereby granted, free of charge',
                r'THE SOFTWARE IS PROVIDED "AS IS"',
            ],
            'risk_level': 'low',
            'risk_color': 'green',
            'description': '非常寬鬆的授權，可商業使用，不強制開源',
            'compatibility': 'excellent',
        },
        {
            'id': 'APACHE-2.0',
            'name': 'Apache License 2.0',
            'patterns': [
                r'Apache License',
                r'Version 2\.0',
                r'http://www\.apache\.org/licenses/LICENSE-2\.0',
            ],
            'risk_level': 'low',
            'risk_color': 'green',
            'description': '寬鬆授權，但需要保留版權聲明和修改說明',
            'compatibility': 'excellent',
        },
        {
            'id': 'BSD-3-CLAUSE',
            'name': 'BSD 3-Clause License',
            'patterns': [
                r'BSD.*3-Clause',
                r'Redistribution and use in source and binary forms',
                r'Neither the name of.*nor the names of its contributors',
            ],
            'risk_level': 'low',
            'risk_color': 'green',
            'description': '寬鬆授權，類似 MIT',
            'compatibility': 'excellent',
        },
        {
            'id': 'BSD-2-CLAUSE',
            'name': 'BSD 2-Clause License',
            'patterns': [
                r'BSD.*2-Clause',
                r'Redistribution and use in source and binary forms',
            ],
            'risk_level': 'low',
            'risk_color': 'green',
            'description': '更簡化的 BSD 授權',
            'compatibility': 'excellent',
        },
        {
            'id': 'ISC',
            'name': 'ISC License',
            'patterns': [
                r'ISC License',
                r'Permission to use, copy, modify',
            ],
            'risk_level': 'low',
            'risk_color': 'green',
            'description': '類似 MIT 的簡短授權',
            'compatibility': 'excellent',
        },
        {
            'id': 'GPL-2.0',
            'name': 'GNU General Public License v2.0',
            'patterns': [
                r'GNU GENERAL PUBLIC LICENSE',
                r'Version 2',
                r'Free Software Foundation',
            ],
            'risk_level': 'high',
            'risk_color': 'red',
            'description': '強制開源！使用此授權的程式碼，你的專案也必須開源',
            'compatibility': 'poor',
        },
        {
            'id': 'GPL-3.0',
            'name': 'GNU General Public License v3.0',
            'patterns': [
                r'GNU GENERAL PUBLIC LICENSE',
                r'Version 3',
                r'Free Software Foundation',
            ],
            'risk_level': 'high',
            'risk_color': 'red',
            'description': '強制開源！比 GPL-2.0 更嚴格',
            'compatibility': 'poor',
        },
        {
            'id': 'AGPL-3.0',
            'name': 'GNU Affero General Public License v3.0',
            'patterns': [
                r'GNU AFFERO GENERAL PUBLIC LICENSE',
                r'Version 3',
            ],
            'risk_level': 'high',
            'risk_color': 'red',
            'description': '超強制開源！連網路服務也要開源',
            'compatibility': 'very-poor',
        },
        {
            'id': 'LGPL-2.1',
            'name': 'GNU Lesser General Public License v2.1',
            'patterns': [
                r'GNU LESSER GENERAL PUBLIC LICENSE',
                r'Version 2\.1',
            ],
            'risk_level': 'medium',
            'risk_color': 'yellow',
            'description': '部分開源要求，使用函式庫可以不開源，但修改它要開源',
            'compatibility': 'moderate',
        },
        {
            'id': 'LGPL-3.0',
            'name': 'GNU Lesser General Public License v3.0',
            'patterns': [
                r'GNU LESSER GENERAL PUBLIC LICENSE',
                r'Version 3',
            ],
            'risk_level': 'medium',
            'risk_color': 'yellow',
            'description': '部分開源要求，比 LGPL-2.1 稍微嚴格',
            'compatibility': 'moderate',
        },
        {
            'id': 'MPL-2.0',
            'name': 'Mozilla Public License 2.0',
            'patterns': [
                r'Mozilla Public License',
                r'Version 2\.0',
            ],
            'risk_level': 'medium',
            'risk_color': 'yellow',
            'description': '檔案層級的開源要求，修改的檔案要開源',
            'compatibility': 'moderate',
        },
        {
            'id': 'UNLICENSE',
            'name': 'The Unlicense',
            'patterns': [
                r'This is free and unencumbered software',
                r'released into the public domain',
            ],
            'risk_level': 'low',
            'risk_color': 'green',
            'description': '公共領域，完全自由使用',
            'compatibility': 'excellent',
        }
    ]
    
    def __init__(self):
        """初始化資料庫"""
        # 編譯所有的正規表示式（提升效能）
        for license_info in self.LICENSES:
            license_info['compiled_patterns'] = [
                re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                for pattern in license_info['patterns']
            ]
    
    def identify_license(self, text: str) -> List[Dict]:
        """
        識別授權類型
        
        Args:
            text: 授權文字內容
            
        Returns:
            可能的授權列表（按信心度排序）
        """
        results = []
        
        for license_info in self.LICENSES:
            # 計算有多少個模式被匹配
            matches = 0
            total_patterns = len(license_info['compiled_patterns'])
            
            for pattern in license_info['compiled_patterns']:
                if pattern.search(text):
                    matches += 1
            
            # 計算信心度（百分比）
            confidence = (matches / total_patterns) * 100
            
            # 只保留信心度 > 50% 的結果
            if confidence > 50:
                results.append({
                    'id': license_info['id'],
                    'name': license_info['name'],
                    'confidence': confidence,
                    'risk_level': license_info['risk_level'],
                    'risk_color': license_info['risk_color'],
                    'description': license_info['description'],
                    'compatibility': license_info['compatibility'],
                })
        
        # 按信心度排序（高到低）
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results
    
    def get_license_by_id(self, license_id: str) -> Dict:
        """根據 ID 取得授權資訊"""
        for license_info in self.LICENSES:
            if license_info['id'] == license_id:
                return license_info
        return None


# 測試程式碼
if __name__ == '__main__':
    db = LicenseDatabase()
    
    # 測試 MIT 授權
    mit_text = """
    MIT License
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
    """
    
    print("測試 MIT 授權識別:")
    results = db.identify_license(mit_text)
    for result in results:
        print(f"  {result['name']}: {result['confidence']:.1f}% 信心度")