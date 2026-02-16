
import React from 'react';
import { Sidebar } from './Sidebar';

export const AppLayout = ({
    children,
    config,
    onConfigChange,
    onLoadModel,
    onUnloadModel,
    modelLoading,
    modelLoaded
}) => {
    return (
        <div className="flex h-screen overflow-hidden bg-[#050505] text-white">
            <Sidebar
                config={config}
                onConfigChange={onConfigChange}
                onLoadModel={onLoadModel}
                onUnloadModel={onUnloadModel}
                modelLoading={modelLoading}
                modelLoaded={modelLoaded}
            />
            <div className="flex-1 flex flex-col h-full relative overflow-hidden bg-dot-pattern">
                {/* Ambient background effects */}
                <div className="absolute top-0 left-0 right-0 h-96 bg-gradient-to-b from-violet-900/10 to-transparent pointer-events-none" />

                <main className="flex-1 overflow-y-auto relative z-10 scroll-smooth">
                    <div className="max-w-7xl mx-auto p-6 md:p-8 lg:p-10 space-y-8 pb-32">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};
