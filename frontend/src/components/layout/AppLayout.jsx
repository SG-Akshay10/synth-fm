
import React from 'react';
import { Sidebar } from './Sidebar';

export const AppLayout = ({
    children,
    config,
    onConfigChange,
    onModelLoad,
    onModelUnload,
    modelLoading,
    loadedModel
}) => {
    return (
        <div className="flex h-screen overflow-hidden bg-transparent text-white">
            <Sidebar
                config={config}
                onConfigChange={onConfigChange}
                onModelLoad={onModelLoad}
                onModelUnload={onModelUnload}
                modelLoading={modelLoading}
                loadedModel={loadedModel}
            />
            <div className="flex-1 flex flex-col h-full relative overflow-hidden">
                {/* Ambient background effects */}
                <div className="absolute top-[-20%] left-[20%] w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] pointer-events-none opacity-40 mix-blend-screen" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-accent/10 rounded-full blur-[100px] pointer-events-none opacity-30 mix-blend-screen" />

                <main className="flex-1 overflow-y-auto relative z-10 scroll-smooth">
                    <div className="max-w-7xl mx-auto p-6 md:p-8 lg:p-10 space-y-8 pb-32">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};
