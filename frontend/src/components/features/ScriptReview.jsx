import React from 'react';
import { Share, Play, Sparkles, FileText } from 'lucide-react';
import { GlassCard } from '../ui/GlassCard';
import { GradientButton } from '../ui/GradientButton';
import { motion } from 'framer-motion';

const SPEAKER_COLORS = [
    {
        bg: 'bg-blue-600',
        text: 'text-white',
        border: 'border-blue-400',
        bubble: 'bg-blue-900/60 border-blue-500/30 text-white'
    },
    {
        bg: 'bg-green-600',
        text: 'text-white',
        border: 'border-green-400',
        bubble: 'bg-green-900/60 border-green-500/30 text-white'
    },
    {
        bg: 'bg-red-600',
        text: 'text-white',
        border: 'border-red-400',
        bubble: 'bg-red-900/60 border-red-500/30 text-white'
    },
    {
        bg: 'bg-orange-600',
        text: 'text-white',
        border: 'border-orange-400',
        bubble: 'bg-orange-900/60 border-orange-500/30 text-white'
    }
];

export const ScriptReview = ({ content, script, onGenerateScript, onSynthesize, loading, speakers }) => {
    return (
        <div className="space-y-6">

            {/* Extracted Content View */}
            {content && !script && (
                <GlassCard>
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-2">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400">
                                <FileText size={18} />
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-white">Content Analysis</h3>
                                <span className="text-xs text-blue-300 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20">
                                    {content.total_word_count} words
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="bg-black/30 rounded-lg p-4 max-h-[200px] overflow-y-auto border border-white/5 text-sm text-gray-300 font-mono custom-scrollbar mb-6">
                        {content.combined_content}
                    </div>

                    <GradientButton
                        onClick={onGenerateScript}
                        loading={loading}
                        className="w-full"
                        variant="primary"
                    >
                        <Sparkles size={16} /> Generate Podcast Script
                    </GradientButton>
                </GlassCard>
            )}

            {/* Script View */}
            {script && (
                <GlassCard className="relative overflow-visible">
                    {/* Decorative Glow */}
                    <div className="absolute -top-10 -right-10 w-40 h-40 bg-purple-500/20 rounded-full blur-3xl pointer-events-none" />

                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                                <Sparkles size={18} />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Generated Script</h3>
                        </div>
                    </div>

                    <div className="space-y-4 mb-8 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                        {script.dialogue.map((turn, i) => {
                            const speakerIndex = speakers.findIndex(s => s.name === turn.speaker);
                            const colorTheme = SPEAKER_COLORS[speakerIndex % SPEAKER_COLORS.length] || SPEAKER_COLORS[0];
                            const isRight = speakerIndex % 2 !== 0;

                            return (
                                <motion.div
                                    initial={{ opacity: 0, x: isRight ? 10 : -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: i * 0.05 }}
                                    key={i}
                                    className={`flex gap-3 sm:gap-4 ${isRight ? 'flex-row-reverse' : 'flex-row'}`}
                                >
                                    <div className={`
                       w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0
                       ${colorTheme.bg} ${colorTheme.text} border ${colorTheme.border}
                    `}>
                                        {turn.speaker.charAt(0)}
                                    </div>
                                    <div className={`
                       flex-1 p-3 rounded-2xl text-sm leading-relaxed border
                       ${colorTheme.bubble}
                       ${isRight ? 'rounded-tr-none' : 'rounded-tl-none'}
                    `}>
                                        <div className="text-xs font-semibold mb-1 opacity-50">{turn.speaker}</div>
                                        {turn.text}
                                    </div>
                                </motion.div>
                            );
                        })}
                    </div>

                    <GradientButton
                        onClick={onSynthesize}
                        loading={loading}
                        className="w-full py-3"
                        variant="primary"
                    >
                        <Play size={18} fill="currentColor" /> Synthesize Audio
                    </GradientButton>
                </GlassCard>
            )}
        </div>
    );
};
