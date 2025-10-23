#!/usr/bin/env python3
"""
Git License Scanner - 第五版（加入 JSON 輸出）
"""

import click
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from .scanner import LicenseScanner

console = Console()

def format_json_output(results):
    """格式化 JSON 輸出"""
    output = {
        'scan_path': results['path'],
        'summary': results['summary'],
        'files': []
    }
    
    for file_info in results['license_files']:
        file_output = {
            'name': file_info['name'],
            'path': file_info['path'],
            'size': file_info['size'],
            'licenses': []
        }
        
        for lic in file_info['identified_licenses']:
            file_output['licenses'].append({
                'id': lic['id'],
                'name': lic['name'],
                'confidence': round(lic['confidence'], 2),
                'risk_level': lic['risk_level'],
                'description': lic['description']
            })
        
        output['files'].append(file_output)
    
    return output

@click.command()
@click.argument('path', default='.')
@click.option('--verbose', '-v', is_flag=True, help='顯示詳細資訊')
@click.option('--show-content', is_flag=True, help='顯示授權檔案內容')
@click.option('--output', '-o', type=click.Choice(['text', 'json']), default='text', help='輸出格式')
@click.option('--output-file', type=click.Path(), help='輸出到檔案')
def scan(path, verbose, show_content, output, output_file):
    """掃描指定路徑的授權資訊"""
    
    # 執行掃描
    scanner = LicenseScanner(path)
    results = scanner.scan()
    
    # JSON 輸出模式
    if output == 'json':
        json_output = format_json_output(results)
        json_str = json.dumps(json_output, indent=2, ensure_ascii=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            console.print(f"[green]✓[/green] JSON 報告已儲存至: {output_file}")
        else:
            print(json_str)
        return
    
    # 文字輸出模式（原有的顯示邏輯）
    # 標題
    console.print(Panel.fit(
        "🔍 Git License Scanner v0.5",
        subtitle="授權識別與風險評估",
        style="bold blue"
    ))
    
    console.print(f"\n[yellow]正在掃描:[/yellow] [cyan]{path}[/cyan]\n")
    
    # 顯示結果
    license_files = results['license_files']
    summary = results['summary']
    
    if not license_files:
        console.print("[red]✗[/red] 未找到 LICENSE 檔案")
        console.print("[dim]提示: 請確認目錄中是否有 LICENSE 或 COPYING 檔案[/dim]\n")
        return
    
    # 找到授權檔案
    console.print(f"[green]✓[/green] 找到 {len(license_files)} 個授權檔案\n")
    
    # 顯示每個檔案的識別結果
    for file_info in license_files:
        # 檔案資訊
        console.print(f"[bold cyan]📄 {file_info['name']}[/bold cyan]")
        console.print(f"   路徑: [dim]{file_info['path']}[/dim]")
        console.print(f"   大小: {file_info['size']} bytes\n")
        
        # 授權識別結果
        licenses = file_info['identified_licenses']
        
        if not licenses:
            console.print("   [red]⚠ 無法識別授權類型[/red]\n")
            continue
        
        # 檢查信心度，顯示警告
        top_license = licenses[0]
        confidence = top_license['confidence']
        
        if confidence < 50:
            console.print("   [red]⚠️⚠️ 嚴重警告: 識別結果信心度很低（< 50%）[/red]")
            console.print("   [dim]建議: 強烈建議手動檢查授權檔案[/dim]\n")
        elif confidence < 70:
            console.print("   [yellow]⚠️ 警告: 識別結果信心度較低（< 70%）[/yellow]")
            console.print("   [dim]建議: 請手動確認授權類型[/dim]\n")
        
        # 建立授權表格
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.SIMPLE,
            padding=(0, 1)
        )
        table.add_column("授權類型", style="cyan")
        table.add_column("信心度", justify="right")
        table.add_column("風險等級", justify="center")
        table.add_column("相容性", justify="center")
        
        for lic in licenses[:3]:  # 只顯示前 3 個最可能的
            # 風險等級顯示
            risk_display = {
                'low': '[green]低 ✓[/green]',
                'medium': '[yellow]中 ⚠[/yellow]',
                'high': '[red]高 ✗[/red]',
            }.get(lic['risk_level'], lic['risk_level'])
            
            # 相容性顯示
            compat_display = {
                'excellent': '[green]優秀[/green]',
                'moderate': '[yellow]普通[/yellow]',
                'poor': '[red]差[/red]',
                'very-poor': '[red]很差[/red]',
            }.get(lic['compatibility'], lic['compatibility'])
            
            table.add_row(
                lic['name'],
                f"{lic['confidence']:.1f}%",
                risk_display,
                compat_display
            )
        
        console.print(table)
        
        # 顯示最可能的授權說明
        if verbose and licenses:
            top_license = licenses[0]
            console.print(f"\n   [bold]說明:[/bold] {top_license['description']}")
        
        console.print()
        
        # 顯示檔案內容
        if show_content and file_info['content']:
            console.print(f"   [yellow]檔案內容（前 500 字元）:[/yellow]")
            content_preview = file_info['content'][:500]
            console.print(Panel(content_preview, border_style="dim"))
            console.print()
    
    # 摘要統計
    console.print("\n[bold]📊 掃描摘要:[/bold]")
    console.print(f"   總檔案數: {summary['total_files']}")
    console.print(f"   已識別: {summary['identified']}")
    console.print(f"   [red]高風險: {summary['high_risk']}[/red]")
    console.print(f"   [yellow]中風險: {summary['medium_risk']}[/yellow]")
    console.print(f"   [green]低風險: {summary['low_risk']}[/green]")
    
    # 風險評估
    console.print("\n[bold]⚖️ 風險評估:[/bold]")
    if summary['high_risk'] > 0:
        console.print("   [red]⚠ 警告: 發現高風險授權！[/red]")
        console.print("   [dim]建議: 檢查這些授權是否與您的專案相容[/dim]")
    elif summary['medium_risk'] > 0:
        console.print("   [yellow]⚠ 注意: 發現中等風險授權[/yellow]")
        console.print("   [dim]建議: 了解這些授權的使用限制[/dim]")
    else:
        console.print("   [green]✓ 良好: 所有授權都是低風險[/green]")
    
    console.print("\n[bold green]✅ 掃描完成！[/bold green]\n")

if __name__ == '__main__':
    scan()