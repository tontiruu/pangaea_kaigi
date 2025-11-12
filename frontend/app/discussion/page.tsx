/**
 * Discussion Page
 */
'use client';

import { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { TopicInput } from '@/components/input/TopicInput';
import { ChatContainer } from '@/components/chat/ChatContainer';
import { SourceStatusBadge } from '@/components/context/SourceStatusBadge';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCircle,
  faLightbulb,
  faVoteYea,
  faHandshake,
  faClipboardList,
  faUsers,
  faCheckCircle,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

export default function DiscussionPage() {
  const [started, setStarted] = useState(false);
  const [showVotingResult, setShowVotingResult] = useState(true);
  const wsUrl = 'ws://localhost:8000/ws/discussion';

  const {
    connected,
    topic,
    agenda,
    agents,
    messages,
    currentPhase,
    currentAgendaIndex,
    votingResult,
    finalConclusion,
    error,
    connect,
    startDiscussion,
  } = useWebSocket(wsUrl);

  useEffect(() => {
    connect();
  }, [connect]);

  const handleStartDiscussion = (newTopic: string) => {
    setStarted(true);
    startDiscussion(newTopic);
  };

  return (
    <div className="h-screen flex flex-col gradient-mesh">
      {/* Header */}
      <header className="glass border-b border-white/10 animate-slide-down">
        <div className="max-w-7xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center shadow-lg">
                <FontAwesomeIcon icon={faUsers} className="text-white text-lg" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 tracking-tight">
                  Pangaea Kaigi
                </h1>
                <p className="text-xs text-gray-500">AI Discussion System</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <SourceStatusBadge />
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/60 backdrop-blur-sm border border-white/20">
                <FontAwesomeIcon
                  icon={faCircle}
                  className={`text-xs transition-all duration-300 ${
                    connected
                      ? 'text-emerald-500'
                      : 'text-red-500'
                  }`}
                  style={{
                    filter: connected
                      ? 'drop-shadow(0 0 4px rgba(16,185,129,0.6))'
                      : 'drop-shadow(0 0 4px rgba(239,68,68,0.6))',
                    animation: connected ? 'pulse-glow 2s infinite' : 'none'
                  }}
                />
                <span className="text-xs font-medium text-gray-700">
                  {connected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
          </div>
          {topic && (
            <div className="mt-3 px-4 py-2 rounded-lg bg-gradient-to-r from-emerald-50 to-teal-50 border border-[#00D4A8]/30 animate-card-pop" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium" style={{ color: 'var(--primary-dark)' }}>Topic</span>
                <span className="text-sm font-semibold text-gray-800">{topic}</span>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Sidebar: Agenda and Participants */}
      {started && (
        <div className="flex flex-1 overflow-hidden">
          <aside className="w-80 glass border-r border-white/10 overflow-y-auto animate-slide-in">
            {/* Agenda */}
            {agenda.length > 0 && (
              <div className="p-5 border-b border-white/10">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-1 h-5 rounded-full" style={{ background: 'linear-gradient(to bottom, var(--primary), var(--primary-dark))' }}></div>
                  <h3 className="font-bold text-gray-800 text-sm tracking-wide uppercase">Agenda</h3>
                </div>
                <div className="space-y-2.5">
                  {agenda.map((item, index) => (
                    <div
                      key={item.id}
                      className={`group p-4 rounded-xl text-sm transition-all duration-500 animate-card-lift ${
                        index === currentAgendaIndex
                          ? 'shadow-xl scale-[1.02] hover:scale-[1.04]'
                          : 'bg-white/50 hover:bg-white/70 backdrop-blur-sm border border-white/30 hover:shadow-xl hover:scale-[1.02] hover:-translate-y-1'
                      }`}
                      style={
                        index === currentAgendaIndex
                          ? {
                              background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))',
                              boxShadow: '0 20px 25px -5px rgba(0, 212, 168, 0.2), 0 10px 10px -5px rgba(0, 212, 168, 0.1)',
                              animationDelay: `${index * 80}ms`
                            }
                          : {
                              animationDelay: `${index * 80}ms`
                            }
                      }
                    >
                      <div className={`font-semibold mb-1 ${
                        index === currentAgendaIndex ? 'text-white' : 'text-gray-800'
                      }`}>
                        <span
                          className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs mr-2 ${
                            index === currentAgendaIndex ? '' : ''
                          }`}
                          style={
                            index === currentAgendaIndex
                              ? { backgroundColor: 'rgba(255, 255, 255, 0.2)' }
                              : { backgroundColor: 'rgba(0, 212, 168, 0.1)', color: 'var(--primary-dark)' }
                          }
                        >
                          {item.order}
                        </span>
                        {item.title}
                      </div>
                      <div className={`text-xs mt-2 leading-relaxed ${
                        index === currentAgendaIndex ? 'text-white/90' : 'text-gray-600'
                      }`}>
                        {item.description}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Participants */}
            {agents.length > 0 && (
              <div className="p-5">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-1 h-5 rounded-full" style={{ background: 'linear-gradient(to bottom, var(--primary-light), var(--primary))' }}></div>
                  <h3 className="font-bold text-gray-800 text-sm tracking-wide uppercase">
                    Participants
                  </h3>
                  <span className="ml-auto px-2 py-0.5 text-white text-xs font-bold rounded-full" style={{ background: 'linear-gradient(to right, var(--primary), var(--primary-dark))' }}>
                    {agents.length}
                  </span>
                </div>
                <div className="space-y-2.5">
                  {agents.map((agent, index) => (
                    <div
                      key={agent.id}
                      className="group p-4 bg-white/50 backdrop-blur-sm border border-white/30 rounded-xl text-sm hover:bg-white/70 hover:shadow-xl hover:-translate-y-1 hover:scale-[1.02] transition-all duration-500 animate-float-up cursor-pointer"
                      style={{
                        animationDelay: `${index * 80}ms`
                      }}
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <div className="w-9 h-9 rounded-lg flex items-center justify-center text-white font-bold text-sm shadow-md" style={{ background: 'linear-gradient(to bottom right, var(--primary-light), var(--primary-dark))' }}>
                          {agent.name.charAt(0)}
                        </div>
                        <div className="font-semibold text-gray-800">{agent.name}</div>
                      </div>
                      <div className="text-xs text-gray-600 leading-relaxed pl-12">
                        {agent.perspective}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </aside>

          {/* Main chat area */}
          <main className="flex-1 flex flex-col">
            {/* Phase display */}
            {currentPhase && (
              <div className="backdrop-blur-sm px-6 py-4 border-b border-white/10 animate-slide-down" style={{ background: 'linear-gradient(to right, rgba(0, 212, 168, 0.08), rgba(51, 224, 186, 0.08))' }}>
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-2">
                    <FontAwesomeIcon icon={faCircle} className="text-xs animate-pulse" style={{ color: 'var(--primary)' }} />
                    <span className="text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Current Phase
                    </span>
                  </div>
                  <span className="px-4 py-1.5 bg-white/70 backdrop-blur-sm rounded-full font-bold text-sm text-gray-800 shadow-sm border border-white/30 flex items-center gap-2">
                    {currentPhase === 'independent_opinions' && (
                      <>
                        <FontAwesomeIcon icon={faLightbulb} style={{ color: 'var(--accent-warning)' }} />
                        Independent Opinions
                      </>
                    )}
                    {currentPhase === 'voting' && (
                      <>
                        <FontAwesomeIcon icon={faVoteYea} style={{ color: 'var(--primary)' }} />
                        Voting
                      </>
                    )}
                    {currentPhase === 'persuasion' && (
                      <>
                        <FontAwesomeIcon icon={faHandshake} style={{ color: 'var(--primary-dark)' }} />
                        Persuasion Process
                      </>
                    )}
                    {currentPhase === 'agenda_creation' && (
                      <>
                        <FontAwesomeIcon icon={faClipboardList} style={{ color: 'var(--primary)' }} />
                        Agenda Creation
                      </>
                    )}
                    {currentPhase === 'agent_generation' && (
                      <>
                        <FontAwesomeIcon icon={faUsers} style={{ color: 'var(--primary-dark)' }} />
                        Participant Selection
                      </>
                    )}
                  </span>
                </div>
              </div>
            )}

            {/* Voting results display */}
            {votingResult && votingResult.opinions && votingResult.opinions.length > 0 && (
              <div className="backdrop-blur-sm border-b border-white/10 animate-slide-down" style={{ background: 'linear-gradient(to right, rgba(0, 212, 168, 0.08), rgba(51, 224, 186, 0.08))', animationDelay: '0.1s' }}>
                <button
                  onClick={() => setShowVotingResult(!showVotingResult)}
                  className="w-full px-6 py-4 flex items-center justify-between hover:bg-white/20 transition-all duration-500 group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center shadow-md" style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}>
                      <FontAwesomeIcon icon={faVoteYea} className="text-white text-sm" />
                    </div>
                    <h3 className="font-bold text-gray-800 text-sm">
                      Voting Results
                    </h3>
                  </div>
                  <span className="text-gray-600 text-sm font-medium transition-transform group-hover:scale-110">
                    {showVotingResult ? '▼ Close' : '▶ Open'}
                  </span>
                </button>

                {showVotingResult && (
                  <div className="px-6 pb-5 space-y-2.5">
                    {votingResult.opinions
                      .filter((op) => op.votes > 0)
                      .sort((a, b) => b.votes - a.votes)
                      .map((opinion, index) => {
                        // Get voters for this opinion
                        const voters = votingResult.vote_details
                          .filter((v) => v.opinion_id === opinion.id)
                          .map((v) => v.voter_name);

                        return (
                          <div
                            key={opinion.id}
                            className="bg-white/70 backdrop-blur-sm px-5 py-3 rounded-xl shadow-md border border-white/30 hover:shadow-xl hover:-translate-y-1 hover:scale-[1.02] transition-all duration-500 animate-card-pop cursor-pointer"
                            style={{
                              animationDelay: `${index * 100}ms`
                            }}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-3 flex-1">
                                <div
                                  className="flex items-center justify-center w-7 h-7 rounded-lg font-bold text-white shadow-md"
                                  style={{
                                    background:
                                      index === 0
                                        ? 'linear-gradient(to bottom right, #FFA726, #FF6F00)'
                                        : index === 1
                                        ? 'linear-gradient(to bottom right, #9CA3AF, #6B7280)'
                                        : index === 2
                                        ? 'linear-gradient(to bottom right, #FFB74D, #FB8C00)'
                                        : 'linear-gradient(to bottom right, var(--primary-light), var(--primary-dark))'
                                  }}
                                >
                                  {index + 1}
                                </div>
                                <div>
                                  <span className="text-sm font-semibold text-gray-800">
                                    {opinion.agent_name}
                                  </span>
                                  <div className="flex items-center gap-2 mt-0.5">
                                    <span className="text-xs font-bold" style={{ color: 'var(--primary-dark)' }}>
                                      {opinion.votes} votes
                                    </span>
                                    {voters.length > 0 && (
                                      <span className="text-xs text-gray-500">
                                        ← {voters.join(', ')}
                                      </span>
                                    )}
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                  </div>
                )}
              </div>
            )}

            <ChatContainer messages={messages} />

            {/* Final conclusion */}
            {finalConclusion && (
              <div className="p-8 border-t border-white/30 animate-float-up" style={{ background: 'linear-gradient(to bottom right, rgba(0, 212, 168, 0.1), rgba(51, 224, 186, 0.1))' }}>
                <div className="max-w-4xl mx-auto">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg animate-bounce-subtle" style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}>
                      <FontAwesomeIcon icon={faCheckCircle} className="text-white text-lg" />
                    </div>
                    <h3 className="font-bold text-xl text-gray-800">
                      Final Conclusion
                    </h3>
                  </div>
                  <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/30">
                    <div className="text-sm text-gray-800 whitespace-pre-wrap leading-relaxed">
                      {finalConclusion}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </main>
        </div>
      )}

      {/* Initial screen: Topic input */}
      {!started && (
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="animate-float-up" style={{ animationDelay: '0.2s' }}>
            <TopicInput
              onSubmit={handleStartDiscussion}
              disabled={!connected || started}
            />
          </div>
        </div>
      )}

      {/* Error display */}
      {error && (
        <div className="fixed bottom-6 right-6 text-white px-6 py-4 rounded-2xl shadow-2xl border border-white/20 backdrop-blur-sm animate-card-pop" style={{ background: 'linear-gradient(to right, var(--accent-error), #D32F2F)' }}>
          <div className="flex items-center gap-3">
            <FontAwesomeIcon icon={faExclamationTriangle} className="text-lg" />
            <span className="font-medium">{error}</span>
          </div>
        </div>
      )}
    </div>
  );
}
