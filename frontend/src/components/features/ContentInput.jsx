import React from 'react';
import { Plus, Trash2, Upload, Link as LinkIcon, FileText } from 'lucide-react';
import { GlassCard } from '../ui/GlassCard';
import { GradientButton } from '../ui/GradientButton';
import { motion, AnimatePresence } from 'framer-motion';

export const ContentInput = ({
    urls,
    onUrlChange,
    onAddUrl,
    onRemoveUrl,
    files,
    onFileChange,
    onProcess,
    loading
}) => {
    return (
        <GlassCard className="w-full">
            <div className="flex items-center gap-3 mb-6">
                <div className="w-8 h-8 rounded-full bg-violet-500/20 flex items-center justify-center text-violet-400">
                    <Upload size={18} />
                </div>
                <div>
                    <h2 className="text-xl font-semibold text-white">Source Material</h2>
                    <p className="text-sm text-gray-400">Upload documents or provide URLs to generate your podcast.</p>
                </div>
            </div>

            <div className="space-y-6">
                {/* URL Section */}
                <div className="space-y-3">
                    <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-1">Web Sources</label>
                    <AnimatePresence>
                        {urls.map((url, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="flex gap-2"
                            >
                                <div className="relative flex-1 group">
                                    <LinkIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-violet-400 transition-colors" />
                                    <input
                                        type="text"
                                        value={url}
                                        onChange={(e) => onUrlChange(i, e.target.value)}
                                        placeholder="https://example.com/article"
                                        className="w-full bg-black/40 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-sm focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all text-white placeholder:text-gray-600"
                                    />
                                </div>
                                {urls.length > 1 && (
                                    <button
                                        onClick={() => onRemoveUrl(i)}
                                        className="w-10 flex items-center justify-center rounded-lg border border-white/5 bg-white/5 text-gray-400 hover:text-red-400 hover:bg-red-500/10 hover:border-red-500/20 transition-all"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    <button
                        onClick={onAddUrl}
                        className="text-xs font-medium text-violet-400 hover:text-violet-300 flex items-center gap-1.5 px-1 py-1 rounded transition-colors"
                    >
                        <Plus size={14} /> Add another URL
                    </button>
                </div>

                {/* File Section */}
                <div className="space-y-3">
                    <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-1">Documents</label>
                    <div className="relative group">
                        <input
                            type="file"
                            multiple
                            onChange={onFileChange}
                            accept=".pdf,.docx,.txt,.md"
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                        />
                        <div className={`
              border-2 border-dashed rounded-xl p-8 transition-all text-center
              ${files.length > 0
                                ? 'border-violet-500/30 bg-violet-500/5'
                                : 'border-white/10 bg-white/5 group-hover:bg-white/10 group-hover:border-white/20'}
            `}>
                            <div className="flex flex-col items-center gap-2">
                                <FileText className={`w-8 h-8 ${files.length > 0 ? 'text-violet-400' : 'text-gray-500'}`} />
                                <div className="text-sm text-gray-300">
                                    {files.length > 0
                                        ? <span className="text-violet-300 font-medium">{files.length} file(s) selected</span>
                                        : <span>Drop files here or click to browse</span>}
                                </div>
                                <div className="text-xs text-gray-500">Supported: PDF, DOCX, TXT, MD</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="pt-2">
                    <GradientButton
                        onClick={onProcess}
                        loading={loading}
                        disabled={(!files.length && !urls[0])}
                        className="w-full py-4 text-base shadow-xl"
                        variant="primary"
                    >
                        Process Source Material
                    </GradientButton>
                </div>

            </div>
        </GlassCard>
    );
};
