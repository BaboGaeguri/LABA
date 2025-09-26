import pandas as pd
import numpy as np

def process_stock_data(df):
    """
    주식 데이터를 처리하여 섹터별 시총가중 수익률과 시가총액을 계산합니다.
    
    Parameters:
    df (pd.DataFrame): 원본 데이터프레임
                      컬럼: 현재날짜, 섹터, 티커, 수익률, 종가, 상장주식수, 시가총액
    
    Returns:
    pd.DataFrame: 섹터별 날짜별 수익률과 시가총액 데이터프레임
    """
    
    # 1단계: 종가와 상장주식수 컬럼 제거
    print("1단계: 불필요한 컬럼 제거")
    processed_df = df.drop(columns=['종가', '상장주식수'], errors='ignore')
    print(f"제거 후 컬럼: {list(processed_df.columns)}")
    
    # 2단계: 섹터별 시가총액 계산
    print("\n2단계: 섹터별 시가총액 계산")
    sector_market_cap = processed_df.groupby(['현재날짜', '섹터'])['시가총액'].sum().reset_index()
    sector_market_cap.rename(columns={'시가총액': '섹터_시가총액'}, inplace=True)
    
    # 원본 데이터에 섹터 시가총액 병합
    processed_df = processed_df.merge(sector_market_cap, on=['현재날짜', '섹터'])
    
    # 3단계: 각 종목의 섹터 내 시가총액 비중 계산
    print("3단계: 섹터 내 시가총액 비중 계산")
    processed_df['시총_비중'] = processed_df['시가총액'] / processed_df['섹터_시가총액']
    
    # 4단계: 시총가중 수익률 계산 (종목별 수익률 × 시총비중)
    print("4단계: 시총가중 수익률 계산")
    processed_df['가중_수익률'] = processed_df['수익률'] * processed_df['시총_비중']
    
    # 5단계: 섹터별로 가중 수익률 합계 계산 (= 섹터별 시총가중 수익률)
    print("5단계: 섹터별 시총가중 수익률 집계")
    sector_returns = processed_df.groupby(['현재날짜', '섹터']).agg({
        '가중_수익률': 'sum',  # 섹터별 시총가중 수익률
        '섹터_시가총액': 'first'  # 섹터 시가총액 (모든 행이 동일하므로 first 사용)
    }).reset_index()
    
    # 컬럼명 정리
    sector_returns.rename(columns={
        '가중_수익률': '섹터_시총가중_수익률',
        '섹터_시가총액': '섹터_시가총액'
    }, inplace=True)
    
    print("\n최종 데이터프레임 생성 완료")
    print(f"최종 컬럼: {list(sector_returns.columns)}")
    
    return sector_returns

def display_summary(df, result_df):
    """데이터 처리 결과 요약 출력"""
    print("\n" + "="*50)
    print("데이터 처리 결과 요약")
    print("="*50)
    
    print(f"원본 데이터: {len(df)}개 행, {len(df.columns)}개 컬럼")
    print(f"처리 후 데이터: {len(result_df)}개 행, {len(result_df.columns)}개 컬럼")
    
    if '현재날짜' in result_df.columns:
        print(f"날짜 범위: {result_df['현재날짜'].min()} ~ {result_df['현재날짜'].max()}")
    
    if '섹터' in result_df.columns:
        print(f"섹터 수: {result_df['섹터'].nunique()}개")
        print(f"섹터 목록: {', '.join(result_df['섹터'].unique())}")
    
    print(f"\n샘플 데이터:")
    print(result_df.head())