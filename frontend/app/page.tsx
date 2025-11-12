'use client';

import Link from "next/link";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUsers,
  faCheckCircle,
  faLightbulb,
  faBolt,
  faChartLine,
  faRocket,
  faArrowRight,
} from '@fortawesome/free-solid-svg-icons';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-teal-50 to-emerald-50 relative overflow-hidden">
      {/* 背景装飾 */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div
          className="absolute top-20 -left-20 w-96 h-96 rounded-full opacity-20 blur-3xl animate-float-up"
          style={{ background: 'radial-gradient(circle, var(--primary), transparent)' }}
        />
        <div
          className="absolute bottom-20 -right-20 w-96 h-96 rounded-full opacity-20 blur-3xl animate-float-up"
          style={{ background: 'radial-gradient(circle, var(--primary-light), transparent)', animationDelay: '1s' }}
        />
      </div>

      <main className="relative flex w-full max-w-7xl mx-auto flex-col items-center gap-16 p-8 py-20">
        {/* ヘッダーセクション */}
        <div className="text-center max-w-4xl animate-fade-in">
          <div
            className="inline-flex items-center justify-center w-20 h-20 rounded-3xl mb-6 shadow-2xl animate-float-up"
            style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}
          >
            <FontAwesomeIcon icon={faUsers} className="text-white text-4xl" />
          </div>

          <h1
            className="text-6xl md:text-7xl font-bold mb-6 bg-clip-text text-transparent leading-tight animate-scale-in"
            style={{
              backgroundImage: 'linear-gradient(to right, var(--primary-dark), var(--primary), var(--primary-light))',
              animationDelay: '0.1s'
            }}
          >
            Pangaea Kaigi
          </h1>

          <p className="text-2xl md:text-3xl font-semibold text-gray-700 mb-4 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            複数のAIエージェントによる
          </p>
          <p className="text-xl md:text-2xl text-gray-600 mb-8 animate-fade-in" style={{ animationDelay: '0.3s' }}>
            高速で緻密な意思決定支援システム
          </p>

          <Link
            href="/discussion"
            className="inline-flex items-center gap-3 px-10 py-5 rounded-2xl font-bold text-white text-xl shadow-2xl hover:shadow-[0_25px_50px_-12px_rgba(0,212,168,0.5)] hover:scale-[1.05] hover:-translate-y-1 transition-all duration-500 group animate-card-pop"
            style={{
              background: 'linear-gradient(to right, var(--primary-dark), var(--primary), var(--primary-light))',
              animationDelay: '0.4s'
            }}
          >
            <FontAwesomeIcon icon={faRocket} className="text-2xl group-hover:rotate-12 transition-transform duration-300" />
            議論を開始する
            <FontAwesomeIcon icon={faArrowRight} className="text-lg group-hover:translate-x-2 transition-transform duration-300" />
          </Link>
        </div>

        {/* 特徴カードグリッド */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-6xl">
          {[
            {
              icon: faUsers,
              title: '多様な視点',
              description: '複数のAIエージェントが異なる観点から意見を出し合う',
              gradient: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))',
              delay: '0.5s'
            },
            {
              icon: faBolt,
              title: '高速プロセス',
              description: '独立した意見出し → 投票 → 説得プロセスで合意形成',
              gradient: 'linear-gradient(to bottom right, var(--primary-light), var(--primary))',
              delay: '0.6s'
            },
            {
              icon: faLightbulb,
              title: 'リアルタイム観察',
              description: '論理的で多角的な意思決定をリアルタイムで観察',
              gradient: 'linear-gradient(to bottom right, var(--primary), var(--primary-lighter))',
              delay: '0.7s'
            },
            {
              icon: faChartLine,
              title: '記録と分析',
              description: '意思決定プロセスが記録され、後から振り返り可能',
              gradient: 'linear-gradient(to bottom right, var(--primary-dark), var(--primary))',
              delay: '0.8s'
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="glass rounded-3xl p-6 border border-white/30 shadow-xl hover:shadow-2xl hover:-translate-y-2 hover:scale-[1.02] transition-all duration-500 animate-card-lift group"
              style={{ animationDelay: feature.delay }}
            >
              <div
                className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 group-hover:rotate-12 transition-all duration-500"
                style={{ background: feature.gradient }}
              >
                <FontAwesomeIcon icon={feature.icon} className="text-white text-2xl" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">{feature.title}</h3>
              <p className="text-sm text-gray-600 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* フッター情報 */}
        {/* <div className="text-center animate-fade-in" style={{ animationDelay: '0.9s' }}>
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-white rounded-2xl shadow-lg border border-gray-200">
            <FontAwesomeIcon icon={faCheckCircle} style={{ color: 'var(--primary)' }} className="text-lg" />
            <span className="text-sm font-semibold text-gray-700">MVP版 - OpenAI GPT-4.1-mini を使用</span>
          </div>
        </div> */}
      </main>
    </div>
  );
}
