import React from 'react';
import { Share, Play, Sparkles } from 'lucide-react';
import { GlassCard } from '../ui/GlassCard';
import { GradientButton } from '../ui/GradientButton';
import { motion } from 'framer-motion';

export const ScriptReview = ({ content, script, onGenerateScript, onSynthesize, loading, speakers }) => {
    return (
        <div className="space-y-6">

            {/* Extracted Content View */}
            {content && !script && (
                <GlassCard>
                    <div className="flex justify-between items-center mb-4">
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
                            const isSpeaker1 = turn.speaker === speakers[0].name;
                            return (
                                <motion.div
                                    initial={{ opacity: 0, x: isSpeaker1 ? -10 : 10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: i * 0.05 }}
                                    key={i}
                                    className={`flex gap-4 ${isSpeaker1 ? 'flex-row' : 'flex-row-reverse'}`}
                                >
                                    <div className={`
                       w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0
                       ${isSpeaker1 ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'bg-pink-500/20 text-pink-300 border border-pink-500/30'}
                    `}>
                                        {turn.speaker.charAt(0)}
                                    </div>
                                    <div className={`
                       flex-1 p-3 rounded-2xl text-sm leading-relaxed
                       ${isSpeaker1
                                            ? 'bg-white/5 rounded-tl-none border border-white/5 text-gray-200'
                                            : 'bg-gradient-to-br from-purple-900/20 to-blue-900/20 rounded-tr-none border border-white/10 text-gray-100'}
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

// Missing icon fix
import { FileText } from 'lucide-react';
