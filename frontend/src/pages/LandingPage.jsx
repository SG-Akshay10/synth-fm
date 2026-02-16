import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mic, Zap, FileText, Headphones, ArrowRight, Github } from 'lucide-react';
import { GradientButton } from '../components/ui/GradientButton';
import { GlassCard } from '../components/ui/GlassCard';

export const LandingPage = () => {
    return (
        <div className="min-h-screen bg-background text-white overflow-hidden relative selection:bg-primary/30">
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-[-20%] left-[20%] w-[800px] h-[800px] bg-primary/20 rounded-full blur-[120px] opacity-40 mix-blend-screen animate-pulse" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-accent/10 rounded-full blur-[100px] opacity-30 mix-blend-screen" />
            </div>

            {/* Navbar */}
            <nav className="relative z-50 flex items-center justify-between px-6 py-6 max-w-7xl mx-auto">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center shadow-[0_0_15px_rgba(98,71,234,0.2)] border border-primary/20">
                        <Mic className="text-primary" size={20} />
                    </div>
                    <span className="font-bold text-xl tracking-tight">Synth-FM</span>
                </div>

                <div className="flex items-center gap-4">
                    <Link to="/app">
                        <GradientButton variant="secondary" className="text-sm px-5 py-2">
                            Launch App
                        </GradientButton>
                    </Link>
                    <a
                        href="https://github.com/SG-Akshay10/synth-fm"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 text-white/60 hover:text-white transition-colors hover:bg-white/10 rounded-lg"
                        title="View on GitHub"
                    >
                        <Github size={20} />
                    </a>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="relative z-10 pt-20 pb-32 px-6">
                <div className="max-w-4xl mx-auto text-center space-y-8">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                    >
                        <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1]">
                            Turn Content into <br />
                            <span className="bg-gradient-to-r from-primary via-white to-accent bg-clip-text text-transparent">
                                Studio-Quality Podcasts
                            </span>
                        </h1>
                    </motion.div>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="text-lg md:text-xl text-white/50 max-w-2xl mx-auto leading-relaxed"
                    >
                        Transform articles, PDFs, and links into engaging audio conversations using advanced AI.
                        Powered by LLMs and neural text-to-speech.
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.4 }}
                        className="flex items-center justify-center gap-4 pt-4"
                    >
                        <Link to="/app">
                            <GradientButton className="text-lg px-8 py-4 h-auto shadow-[0_0_40px_rgba(98,71,234,0.4)] hover:shadow-[0_0_60px_rgba(98,71,234,0.6)]">
                                Start Creating <ArrowRight size={20} />
                            </GradientButton>
                        </Link>
                    </motion.div>
                </div>

                {/* Features Grid */}
                <div id="features" className="max-w-7xl mx-auto mt-32 grid grid-cols-1 md:grid-cols-3 gap-6">
                    <GlassCard className="p-8 space-y-4 hover:bg-white/5 transition-colors group">
                        <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                            <FileText className="text-primary" size={24} />
                        </div>
                        <h3 className="text-xl font-bold">Multi-Format Input</h3>
                        <p className="text-white/50 leading-relaxed">
                            Upload PDFs, text files, or paste URLs. We intelligently extract and process content from any source.
                        </p>
                    </GlassCard>

                    <GlassCard className="p-8 space-y-4 hover:bg-white/5 transition-colors group">
                        <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center group-hover:bg-accent/20 transition-colors">
                            <Zap className="text-accent" size={24} />
                        </div>
                        <h3 className="text-xl font-bold">AI Scriptwriting</h3>
                        <p className="text-white/50 leading-relaxed">
                            Our LLM agents generate natural, engaging dialogues between hosts, optimized for audio retention.
                        </p>
                    </GlassCard>

                    <GlassCard className="p-8 space-y-4 hover:bg-white/5 transition-colors group">
                        <div className="w-12 h-12 rounded-lg bg-indigo-500/10 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors">
                            <Headphones className="text-indigo-400" size={24} />
                        </div>
                        <h3 className="text-xl font-bold">Neural Voice Synthesis</h3>
                        <p className="text-white/50 leading-relaxed">
                            Hyper-realistic AI voices with emotional depth and proper pacing. It sounds just like a real podcast.
                        </p>
                    </GlassCard>
                </div>

                {/* Footerish area */}
                <div className="mt-32 border-t border-white/5 pt-12 text-center text-white/30 text-sm">
                    <p>&copy; 2026 Synth-FM</p>
                </div>
            </main>
        </div>
    );
};
