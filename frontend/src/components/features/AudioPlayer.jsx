import React, { useRef, useState, useEffect } from 'react';
import { Play, Pause, Download, Volume2, SkipBack, SkipForward } from 'lucide-react';
import { GlassCard } from '../ui/GlassCard';
import { motion } from 'framer-motion';

export const AudioPlayer = ({ audioPath, onDownload }) => {
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [progress, setProgress] = useState(0);
    const [volume, setVolume] = useState(1);
    const [currentTime, setCurrentTime] = useState("00:00");
    const [duration, setDuration] = useState("00:00");

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const handleTimeUpdate = () => {
        if (audioRef.current) {
            const current = audioRef.current.currentTime;
            const total = audioRef.current.duration;
            setProgress((current / total) * 100);

            const formatTime = (time) => {
                const min = Math.floor(time / 60);
                const sec = Math.floor(time % 60);
                return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
            };

            setCurrentTime(formatTime(current));
            if (!isNaN(total)) setDuration(formatTime(total));
        }
    };

    const handleSeek = (e) => {
        const width = e.target.clientWidth;
        const clickX = e.nativeEvent.offsetX;
        const duration = audioRef.current.duration;
        audioRef.current.currentTime = (clickX / width) * duration;
    };

    return (
        <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="fixed bottom-0 left-0 right-0 z-50 px-4 pb-6 pt-2"
        >
            <div className="max-w-3xl mx-auto">
                <GlassCard className="!p-4 bg-black/60 backdrop-blur-xl border-violet-500/20 shadow-2xl shadow-violet-900/20">
                    <audio
                        ref={audioRef}
                        src={`http://localhost:8000/api/audio/download-podcast?path=${audioPath}`}
                        onTimeUpdate={handleTimeUpdate}
                        onEnded={() => setIsPlaying(false)}
                        onLoadedMetadata={handleTimeUpdate}
                        autoPlay
                    />

                    <div className="flex items-center gap-4">
                        {/* Info */}
                        <div className="hidden sm:block w-32">
                            <div className="text-sm font-medium text-white truncate">Final Podcast</div>
                            <div className="text-xs text-gray-400">Synth-FM</div>
                        </div>

                        {/* Controls */}
                        <div className="flex-1 flex flex-col items-center gap-2">
                            <div className="flex items-center gap-4">
                                <button onClick={() => audioRef.current.currentTime -= 10} className="text-gray-400 hover:text-white transition-colors"><SkipBack size={20} /></button>
                                <button
                                    onClick={togglePlay}
                                    className="w-10 h-10 rounded-full bg-white text-black flex items-center justify-center hover:scale-105 transition-transform"
                                >
                                    {isPlaying ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" className="ml-1" />}
                                </button>
                                <button onClick={() => audioRef.current.currentTime += 10} className="text-gray-400 hover:text-white transition-colors"><SkipForward size={20} /></button>
                            </div>

                            {/* Progress Bar */}
                            <div className="w-full flex items-center gap-2 text-xs text-gray-400 font-mono">
                                <span>{currentTime}</span>
                                <div
                                    className="flex-1 h-1 bg-white/10 rounded-full cursor-pointer relative group"
                                    onClick={handleSeek}
                                >
                                    <div
                                        className="absolute top-0 left-0 h-full bg-violet-500 rounded-full group-hover:bg-violet-400 transition-colors"
                                        style={{ width: `${progress}%` }}
                                    />
                                </div>
                                <span>{duration}</span>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-2 w-32 justify-end">
                            <div className="group relative hidden sm:flex items-center gap-2">
                                <Volume2 size={18} className="text-gray-400" />
                                <input
                                    type="range" min="0" max="1" step="0.1"
                                    onChange={(e) => {
                                        setVolume(e.target.value);
                                        audioRef.current.volume = e.target.value;
                                    }}
                                    className="w-16 h-1 bg-gray-700 rounded-lg accent-white"
                                />
                            </div>
                            <a
                                href={`http://localhost:8000/api/audio/download-podcast?path=${audioPath}`}
                                download="podcast.wav"
                                className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                            >
                                <Download size={20} />
                            </a>
                        </div>

                    </div>
                </GlassCard>
            </div>
        </motion.div>
    );
};
