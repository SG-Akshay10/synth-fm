import React from 'react';
import { Mic, Settings, Sliders, Box, Cpu, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const Sidebar = ({ config, onConfigChange, onModelLoad, onModelUnload, modelLoading, loadedModel, isOpen, onClose }) => {
    const handleChange = (field, value) => {
        onConfigChange({ ...config, [field]: value });
    };

    const handleSpeakerChange = (index, field, value) => {
        const newSpeakers = [...config.speakers];
        newSpeakers[index] = { ...newSpeakers[index], [field]: value };
        handleChange('speakers', newSpeakers);
    };

    // Helper to verify if configuration has speakers array before mapping
    const speakers = config.speakers || [];

    const isCurrentModelLoaded = loadedModel === config.modelName;

    // Sidebar Content Component
    const SidebarContent = () => (
        <aside className="w-80 bg-background/95 backdrop-blur-2xl border-r border-white/5 h-full flex flex-col shadow-2xl">
            {/* Header */}
            <div className="p-6 border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center shadow-[0_0_15px_rgba(98,71,234,0.2)] border border-primary/20">
                        <Mic className="text-primary" size={20} />
                    </div>
                    <div>
                        <h1 className="font-bold text-lg tracking-tight text-white">
                            Synth-FM
                        </h1>
                        <p className="text-xs text-white/50 font-medium">AI Podcast Generator</p>
                    </div>
                </div>
                {/* Mobile Close Button */}
                <button
                    onClick={onClose}
                    className="md:hidden p-2 text-white/60 hover:text-white transition-colors"
                >
                    <X size={20} />
                </button>
            </div>

            {/* Scrollable Config Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">

                {/* Model Section */}
                <section className="space-y-4">
                    <div className="flex items-center gap-2 text-xs font-bold text-white/40 uppercase tracking-widest">
                        <Cpu size={12} /> Model Provider
                    </div>

                    <div className="grid grid-cols-1 gap-2">
                        {["openai", "gemini", "groq"].map(p => (
                            <label key={p} className={`
                relative flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-300 border
                ${config.provider === p
                                    ? 'bg-primary/10 border-primary/30 shadow-[0_0_15px_rgba(98,71,234,0.1)]'
                                    : 'bg-white/5 border-white/5 hover:bg-white/10 hover:border-white/10'}
              `}>
                                <input
                                    type="radio"
                                    name="provider"
                                    value={p}
                                    checked={config.provider === p}
                                    onChange={(e) => handleChange('provider', e.target.value)}
                                    className="hidden"
                                />
                                <div className={`w-4 h-4 rounded-full border flex items-center justify-center transition-colors duration-300
                  ${config.provider === p ? 'border-primary' : 'border-white/20'}`}>
                                    {config.provider === p && <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_10px_rgba(98,71,234,0.8)]" />}
                                </div>
                                <span className={`capitalize font-medium text-sm transition-colors duration-300 ${config.provider === p ? 'text-white' : 'text-white/60'}`}>{p}</span>
                            </label>
                        ))}
                    </div>

                    {config.provider !== 'local' && (
                        <input
                            type="password"
                            placeholder="API Key"
                            value={config.apiKey}
                            onChange={(e) => handleChange('apiKey', e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-white/20 text-white"
                        />
                    )}

                    <div className="relative">
                        <select
                            value={config.modelName}
                            onChange={(e) => handleChange('modelName', e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-primary/50 transition-all text-white appearance-none cursor-pointer hover:bg-white/10"
                        >
                            {config.provider === 'local' ? (
                                <>
                                    <option value="local_3b" className="bg-[#07001F]">Llama-3.2-3B</option>
                                    <option value="local_1b" className="bg-[#07001F]">Llama-3.2-1B</option>
                                    <option value="local_qwen_1_5b" className="bg-[#07001F]">Qwen2-1.5B</option>
                                </>
                            ) : config.provider === 'openai' ? (
                                <>
                                    <option value="gpt-4o" className="bg-[#07001F]">GPT-4o</option>
                                    <option value="gpt-3.5-turbo" className="bg-[#07001F]">GPT-3.5 Turbo</option>
                                </>
                            ) : config.provider === 'gemini' ? (
                                <>
                                    <option value="gemini-3-flash-preview" className="bg-[#07001F]">Gemini 3 Flash Preview</option>
                                    <option value="gemini-3-pro-preview" className="bg-[#07001F]">Gemini 3 Pro Preview</option>
                                </>
                            ) : (
                                <>
                                    <option value="llama-3.1-8b-instant" className="bg-[#07001F]">Llama 3.1 8B Instant</option>
                                </>
                            )}
                        </select>
                        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-white/40">
                            <Box size={14} />
                        </div>
                    </div>

                    {config.provider === 'local' && (
                        <div className="mt-2 text-center">
                            <div className="flex gap-2">
                                <button
                                    onClick={onModelLoad}
                                    disabled={modelLoading || isCurrentModelLoaded}
                                    className={`flex-1 py-2.5 px-3 rounded-lg text-xs font-bold uppercase tracking-wide transition-all ${isCurrentModelLoaded
                                        ? "bg-accent/10 text-accent border border-accent/20 cursor-default shadow-[0_0_15px_rgba(0,255,128,0.1)]"
                                        : "bg-primary hover:bg-primary/90 text-white shadow-[0_0_20px_rgba(98,71,234,0.3)] hover:shadow-[0_0_30px_rgba(98,71,234,0.5)]"
                                        }`}
                                >
                                    {modelLoading ? (
                                        <span className="flex items-center justify-center gap-2">
                                            <div className="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin" />
                                            Loading...
                                        </span>
                                    ) : isCurrentModelLoaded ? (
                                        "Model Ready"
                                    ) : loadedModel ? (
                                        "Switch Model"
                                    ) : (
                                        "Load Model"
                                    )}
                                </button>
                                {loadedModel && (
                                    <button
                                        onClick={onModelUnload}
                                        className="py-2.5 px-3 rounded-lg text-xs font-bold uppercase tracking-wide bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all hover:shadow-[0_0_15px_rgba(239,68,68,0.2)]"
                                        title="Unload Model to free VRAM"
                                    >
                                        Unload
                                    </button>
                                )}
                            </div>
                            {!isCurrentModelLoaded && <p className="text-[10px] text-white/30 mt-2">Initial load may take a moment</p>}
                        </div>
                    )}
                </section>

                {/* Podcast Settings */}
                <section className="space-y-4">
                    <div className="flex items-center gap-2 text-xs font-bold text-white/40 uppercase tracking-widest">
                        <Sliders size={12} /> Configuration
                    </div>

                    <div className="space-y-1">
                        <label className="text-xs text-white/40 font-medium ml-1">Podcast Name</label>
                        <input
                            type="text"
                            value={config.podcastName}
                            onChange={(e) => handleChange('podcastName', e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-primary/50 transition-all text-white placeholder:text-white/20"
                            placeholder="My Awesome Podcast"
                        />
                    </div>

                    <div className="space-y-3 pt-2">
                        <div className="flex justify-between items-end">
                            <label className="text-xs text-white/40 font-medium ml-1">Duration</label>
                            <span className="text-xs text-primary font-mono bg-primary/10 px-2 py-0.5 rounded border border-primary/20">{config.duration} min</span>
                        </div>
                        <input
                            type="range"
                            min="2" max="10"
                            value={config.duration}
                            onChange={(e) => handleChange('duration', parseInt(e.target.value))}
                            className="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-primary hover:accent-primary/80"
                        />
                    </div>

                    <div className="space-y-3 pt-2">
                        <div className="flex justify-between items-end">
                            <label className="text-xs text-white/40 font-medium ml-1">Speakers</label>
                            <span className="text-xs text-primary font-mono bg-primary/10 px-2 py-0.5 rounded border border-primary/20">{config.numSpeakers}</span>
                        </div>
                        <input
                            type="range"
                            min="2" max="4"
                            value={config.numSpeakers}
                            onChange={(e) => {
                                const num = parseInt(e.target.value);
                                const newSpeakers = [...speakers];
                                if (num > newSpeakers.length) {
                                    for (let i = newSpeakers.length; i < num; i++) {
                                        newSpeakers.push({ name: `Speaker ${i + 1}`, gender: "Female" });
                                    }
                                } else {
                                    newSpeakers.splice(num);
                                }
                                onConfigChange({
                                    ...config,
                                    numSpeakers: num,
                                    speakers: newSpeakers
                                });
                            }}
                            className="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-primary hover:accent-primary/80"
                        />
                    </div>

                    <div className="space-y-2 pt-2">
                        <label className="text-xs text-white/40 font-medium ml-1">Speaker Details</label>
                        {speakers.map((speaker, idx) => (
                            <div key={idx} className="flex gap-2 items-center">
                                <div className="flex-1 flex gap-2 p-1.5 rounded-lg bg-white/5 border border-white/5 focus-within:border-white/10 transition-colors">
                                    <input
                                        value={speaker.name}
                                        onChange={(e) => handleSpeakerChange(idx, 'name', e.target.value)}
                                        className="w-full bg-transparent border-none text-xs text-white focus:outline-none placeholder:text-white/20 pl-2"
                                        placeholder="Name"
                                    />
                                </div>
                                <div className="relative w-24">
                                    <select
                                        value={speaker.gender}
                                        onChange={(e) => handleSpeakerChange(idx, 'gender', e.target.value)}
                                        className="w-full appearance-none bg-white/5 border border-white/5 rounded-lg text-xs text-white/80 focus:outline-none focus:border-primary/30 py-1.5 pl-3 pr-6 cursor-pointer hover:bg-white/10 transition-colors"
                                    >
                                        <option value="Male" className="bg-[#07001F]">Male</option>
                                        <option value="Female" className="bg-[#07001F]">Female</option>
                                    </select>
                                    <div className="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none text-white/40">
                                        <Box size={10} />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                </section>

                {/* Content Style Section */}
                <section className="space-y-4">
                    <div className="flex items-center gap-2 text-xs font-bold text-white/40 uppercase tracking-widest">
                        <Sliders size={12} /> Content Style
                    </div>

                    {/* Tone Selection */}
                    <div className="space-y-2">
                        <label className="text-xs text-white/40 font-medium ml-1">Tone</label>
                        <div className="grid grid-cols-2 gap-2">
                            {["Fun & Engaging", "Informative", "Serious", "Educational", "Casual", "Storytelling"].map(tone => (
                                <button
                                    key={tone}
                                    onClick={() => handleChange('tone', tone)}
                                    className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${config.tone === tone
                                        ? 'bg-primary text-white shadow-[0_0_15px_rgba(98,71,234,0.3)]'
                                        : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
                                        }`}
                                >
                                    {tone}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Custom Instructions */}
                    <div className="space-y-2 pt-2">
                        <label className="flex items-center gap-2 cursor-pointer group">
                            <input
                                type="checkbox"
                                checked={config.useCustomInstructions}
                                onChange={(e) => handleChange('useCustomInstructions', e.target.checked)}
                                className="w-4 h-4 rounded border-white/20 bg-white/5 text-primary focus:ring-primary/50 transition-all"
                            />
                            <span className={`text-xs font-medium transition-colors ${config.useCustomInstructions ? 'text-white' : 'text-white/60 group-hover:text-white/80'}`}>
                                Custom Instructions
                            </span>
                        </label>

                        <AnimatePresence>
                            {config.useCustomInstructions && (
                                <motion.div
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: "auto", opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    className="overflow-hidden"
                                >
                                    <textarea
                                        value={config.customInstructions}
                                        onChange={(e) => handleChange('customInstructions', e.target.value)}
                                        placeholder="E.g., Act like Adam Sandler, focus on the technical details, use simple metaphors..."
                                        className="w-full h-24 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-xs text-white placeholder:text-white/20 focus:outline-none focus:border-primary/50 transition-all resize-none"
                                    />
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </section>
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-white/5 bg-black/20">
                <p className="text-[10px] text-white/30 text-center">v1.0.0 • Yeldra Style</p>
            </div>
        </aside>
    );

    return (
        <>
            {/* Desktop Sidebar */}
            <div className="hidden md:block h-full z-50">
                <SidebarContent />
            </div>

            {/* Mobile Sidebar (Drawer) */}
            <AnimatePresence>
                {isOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={onClose}
                            className="md:hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50"
                        />
                        {/* Drawer */}
                        <motion.div
                            initial={{ x: "-100%" }}
                            animate={{ x: 0 }}
                            exit={{ x: "-100%" }}
                            transition={{ type: "spring", stiffness: 300, damping: 30 }}
                            className="md:hidden fixed inset-y-0 left-0 w-80 z-50"
                        >
                            <SidebarContent />
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
};
