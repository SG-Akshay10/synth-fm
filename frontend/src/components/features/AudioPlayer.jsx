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
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full"
        >
            <GlassCard className="!p-0 overflow-hidden bg-black/40 backdrop-blur-xl border-violet-500/20 shadow-2xl shadow-violet-900/20">
                <div className="p-6 md:p-8 flex flex-col md:flex-row items-center gap-6">

                    {/* Icon/Art Placeholder */}
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 flex items-center justify-center border border-white/10 shrink-0">
                        <Volume2 size={32} className="text-white/80" />
                    </div>

                    <div className="flex-1 w-full space-y-4">
                        <div className="flex justify-between items-start">
                            <div>
                                <h3 className="text-xl font-bold text-white">Final Podcast</h3>
                                <p className="text-sm text-gray-400">Synth-FM • Generated Audio</p>
                            </div>

                            {/* Download Button (Desktop) */}
                            <a
                                href={`http://localhost:8000/api/audio/download-podcast?path=${audioPath}`}
                                download="podcast.wav"
                                className="hidden md:flex items-center gap-2 px-4 py-2 bg-white text-black font-semibold rounded-lg hover:bg-gray-200 transition-colors"
                            >
                                <Download size={18} />
                                Download WAV
                            </a>
                        </div>

                        <div className="flex items-center gap-4">
                            <button onClick={() => audioRef.current.currentTime -= 10} className="text-gray-400 hover:text-white transition-colors"><SkipBack size={20} /></button>
                            <button
                                onClick={togglePlay}
                                className="w-12 h-12 rounded-full bg-white text-black flex items-center justify-center hover:scale-105 transition-transform shadow-lg shadow-white/20"
                            >
                                {isPlaying ? <Pause size={24} fill="currentColor" /> : <Play size={24} fill="currentColor" className="ml-1" />}
                            </button>
                            <button onClick={() => audioRef.current.currentTime += 10} className="text-gray-400 hover:text-white transition-colors"><SkipForward size={20} /></button>

                            {/* Progress & Time */}
                            <div className="flex-1 flex flex-col gap-1">
                                <div
                                    className="h-1.5 bg-white/10 rounded-full cursor-pointer relative group"
                                    onClick={handleSeek}
                                >
                                    <div
                                        className="absolute top-0 left-0 h-full bg-gradient-to-r from-violet-500 to-fuchsia-500 rounded-full group-hover:from-violet-400 group-hover:to-fuchsia-400 transition-all"
                                        style={{ width: `${progress}%` }}
                                    />
                                </div>
                                <div className="flex justify-between text-xs text-gray-500 font-mono">
                                    <span>{currentTime}</span>
                                    <span>{duration}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Mobile Download/Volume Footer */}
                <div className="bg-white/5 border-t border-white/5 p-4 flex items-center justify-between md:justify-end gap-4">
                    <div className="flex items-center gap-2 flex-1 md:flex-none md:w-48">
                        <Volume2 size={16} className="text-gray-400" />
                        <input
                            type="range" min="0" max="1" step="0.1"
                            onChange={(e) => {
                                setVolume(e.target.value);
                                audioRef.current.volume = e.target.value;
                            }}
                            className="w-full h-1 bg-gray-700 rounded-lg accent-white appearance-none cursor-pointer"
                        />
                    </div>

                    <a
                        href={`http://localhost:8000/api/audio/download-podcast?path=${audioPath}`}
                        download="podcast.wav"
                        className="md:hidden flex items-center gap-2 px-4 py-2 bg-white/10 text-white font-medium rounded-lg hover:bg-white/20 transition-colors text-sm"
                    >
                        <Download size={16} />
                        Download
                    </a>
                </div>

                <audio
                    ref={audioRef}
                    src={`http://localhost:8000/api/audio/download-podcast?path=${audioPath}`}
                    onTimeUpdate={handleTimeUpdate}
                    onEnded={() => setIsPlaying(false)}
                    onLoadedMetadata={handleTimeUpdate}
                    autoPlay
                />
            </GlassCard>
        </motion.div>
    );
};
