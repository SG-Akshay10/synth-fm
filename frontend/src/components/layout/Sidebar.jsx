import React from 'react';
import { Mic, Settings, Sliders, Box, Cpu } from 'lucide-react';
import { motion } from 'framer-motion';

export const Sidebar = ({ config, onConfigChange, onLoadModel, onUnloadModel, modelLoading, modelLoaded }) => {
    const handleChange = (field, value) => {
        onConfigChange({ ...config, [field]: value });
    };

    const handleSpeakerChange = (index, field, value) => {
        const newSpeakers = [...config.speakers];
        newSpeakers[index] = { ...newSpeakers[index], [field]: value };
        handleChange('speakers', newSpeakers);
    };

    return (
        <div className="w-80 bg-black/40 backdrop-blur-xl border-r border-white/5 h-full flex flex-col">
            {/* Header */}
            <div className="p-6 border-b border-white/5 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/20">
                    <Mic className="text-white" size={20} />
                </div>
                <div>
                    <h1 className="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                        Synth-FM
                    </h1>
                    <p className="text-xs text-gray-500 font-medium">AI Podcast Generator</p>
                </div>
            </div>

            {/* Scrollable Config Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">

                {/* Model Section */}
                <section className="space-y-4">
                    <div className="flex items-center gap-2 text-sm font-medium text-gray-400 uppercase tracking-wider">
                        <Cpu size={14} /> Model Provider
                    </div>

                    <div className="grid grid-cols-1 gap-2">
                        {["local", "openai", "gemini"].map(p => (
                            <label key={p} className={`
                relative flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200 border
                ${config.provider === p
                                    ? 'bg-white/10 border-violet-500/50 shadow-[0_0_15px_rgba(139,92,246,0.1)]'
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
                                <div className={`w-4 h-4 rounded-full border flex items-center justify-center
                  ${config.provider === p ? 'border-violet-500' : 'border-gray-600'}`}>
                                    {config.provider === p && <div className="w-2 h-2 rounded-full bg-violet-500" />}
                                </div>
                                <span className="capitalize font-medium text-sm text-gray-200">{p}</span>
                            </label>
                        ))}
                    </div>

                    {config.provider !== 'local' && (
                        <input
                            type="password"
                            placeholder="API Key"
                            value={config.apiKey}
                            onChange={(e) => handleChange('apiKey', e.target.value)}
                            className="w-full bg-black/50 border border-white/10 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-violet-500/50 focus:ring-1 focus:ring-violet-500/50 transition-all placeholder:text-gray-600"
                        />
                    )}

                    <select
                        value={config.modelName}
                        onChange={(e) => handleChange('modelName', e.target.value)}
                        className="w-full bg-black/50 border border-white/10 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-violet-500/50 transition-all text-gray-300 appearance-none cursor-pointer hover:bg-white/5"
                    >
                        {config.provider === 'local' ? (
                            <>
                                <option value="local_3b">Llama-3.2-3B</option>
                                <option value="local_1b">Llama-3.2-1B</option>
                            </>
                        ) : config.provider === 'openai' ? (
                            <>
                                <option value="gpt-4o">GPT-4o</option>
                                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                            </>
                        ) : (
                            <>
                                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                            </>
                        )}
                    </select>

                    {config.provider === 'local' && (
                        <div className="mt-2">
                            <div className="flex gap-2">
                                <button
                                    onClick={onLoadModel}
                                    disabled={modelLoading || modelLoaded}
                                    className={`flex-1 py-2.5 px-3 rounded-lg text-xs font-medium transition-all ${modelLoaded
                                        ? "bg-green-500/10 text-green-400 border border-green-500/20 cursor-default"
                                        : "bg-violet-600 hover:bg-violet-500 text-white shadow-lg shadow-violet-900/20"
                                        }`}
                                >
                                    {modelLoading ? (
                                        <span className="flex items-center justify-center gap-2">
                                            <div className="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin" />
                                            Loading...
                                        </span>
                                    ) : modelLoaded ? (
                                        "Model Loaded"
                                    ) : (
                                        "Load Model"
                                    )}
                                </button>
                                {modelLoaded && (
                                    <button
                                        onClick={onUnloadModel}
                                        className="py-2.5 px-3 rounded-lg text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all"
                                        title="Unload Model to free VRAM"
                                    >
                                        Unload
                                    </button>
                                )}
                            </div>
                            {!modelLoaded && <p className="text-[10px] text-gray-500 mt-1.5 text-center">First run may take time to download weights.</p>}
                        </div>
                    )}
                </section>

                {/* Podcast Settings */}
                <section className="space-y-4">
                    <div className="flex items-center gap-2 text-sm font-medium text-gray-400 uppercase tracking-wider">
                        <Sliders size={14} /> Configuration
                    </div>

                    <div className="space-y-1">
                        <label className="text-xs text-gray-500">Podcast Name</label>
                        <input
                            type="text"
                            value={config.podcastName}
                            onChange={(e) => handleChange('podcastName', e.target.value)}
                            className="w-full bg-black/50 border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-violet-500/50 transition-all"
                        />
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between">
                            <label className="text-xs text-gray-500">Duration</label>
                            <span className="text-xs text-violet-400 font-mono">{config.duration} min</span>
                        </div>
                        <input
                            type="range"
                            min="2" max="10"
                            value={config.duration}
                            onChange={(e) => handleChange('duration', parseInt(e.target.value))}
                            className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-violet-500"
                        />
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between">
                            <label className="text-xs text-gray-500">Number of Speakers</label>
                            <span className="text-xs text-violet-400 font-mono">{config.numSpeakers}</span>
                        </div>
                        <input
                            type="range"
                            min="2" max="4"
                            value={config.numSpeakers}
                            onChange={(e) => {
                                const num = parseInt(e.target.value);
                                const newSpeakers = [...config.speakers];
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
                            className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-violet-500"
                        />
                    </div>

                    <div className="space-y-3">
                        <label className="text-xs text-gray-500">Speaker Details</label>
                        {config.speakers.map((speaker, idx) => (
                            <div key={idx} className="flex gap-2 p-2 rounded-lg bg-white/5 border border-white/5">
                                <input
                                    value={speaker.name}
                                    onChange={(e) => handleSpeakerChange(idx, 'name', e.target.value)}
                                    className="w-full bg-transparent border-none text-xs text-white focus:outline-none placeholder:text-gray-600"
                                    placeholder="Name"
                                />
                                <div className="w-px bg-white/10 mx-1" />
                                <select
                                    value={speaker.gender}
                                    onChange={(e) => handleSpeakerChange(idx, 'gender', e.target.value)}
                                    className="bg-transparent border-none text-xs text-gray-400 focus:outline-none cursor-pointer hover:text-white"
                                >
                                    <option value="Male">M</option>
                                    <option value="Female">F</option>
                                </select>
                            </div>
                        ))}
                    </div>

                </section>
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-white/5 bg-black/20">
                <p className="text-[10px] text-gray-600 text-center">v1.0.0 • Powered by LLMs</p>
            </div>
        </div>
    );
};
