import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
      <main className="flex w-full max-w-4xl flex-col items-center gap-12 p-8">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Pangaea Kaigi
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            複数のAIエージェントによる高速で緻密な意思決定支援システム
          </p>
        </div>

        <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            プロダクトの特徴
          </h2>
          <ul className="space-y-3 text-gray-600 mb-8">
            <li className="flex items-start gap-3">
              <span className="text-blue-500 font-bold">✓</span>
              <span>複数のAIエージェントが異なる観点から意見を出し合う</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-blue-500 font-bold">✓</span>
              <span>独立した意見出し → 投票 → 説得プロセスで合意形成</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-blue-500 font-bold">✓</span>
              <span>論理的で多角的な意思決定をリアルタイムで観察</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-blue-500 font-bold">✓</span>
              <span>意思決定プロセスが記録され、後から振り返り可能</span>
            </li>
          </ul>

          <Link
            href="/discussion"
            className="block w-full text-center bg-blue-600 text-white font-semibold py-4 px-8 rounded-lg hover:bg-blue-700 transition-colors text-lg"
          >
            議論を開始する
          </Link>
        </div>

        <div className="text-center text-sm text-gray-500">
          <p>MVP版 - OpenAI GPT-4.1-mini を使用</p>
        </div>
      </main>
    </div>
  );
}
