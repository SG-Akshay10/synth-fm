
import React from 'react';
import { Sidebar } from './Sidebar';
import { Menu } from 'lucide-react';

export const AppLayout = ({
    children,
    config,
    onConfigChange,
    onModelLoad,
    onModelUnload,
    modelLoading,
    loadedModel
}) => {
    const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

    return (
        <div className="flex h-screen overflow-hidden bg-transparent text-white relative">
            {/* Mobile Header for Sidebar Toggle */}
            <div className="md:hidden fixed top-0 left-0 right-0 z-40 h-16 px-4 flex items-center pointer-events-none">
                <button
                    onClick={() => setIsSidebarOpen(true)}
                    className="p-2 -ml-2 text-white/70 hover:text-white pointer-events-auto bg-black/30 rounded-lg"
                >
                    <Menu size={24} />
                </button>
            </div>

            <Sidebar
                config={config}
                onConfigChange={onConfigChange}
                onModelLoad={onModelLoad}
                onModelUnload={onModelUnload}
                modelLoading={modelLoading}
                loadedModel={loadedModel}
                isOpen={isSidebarOpen}
                onClose={() => setIsSidebarOpen(false)}
            />

            <div className="flex-1 flex flex-col h-full relative overflow-hidden transition-all duration-300">
                {/* Ambient background effects */}
                <div className="absolute top-[-20%] left-[20%] w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] pointer-events-none opacity-40 mix-blend-screen" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-accent/10 rounded-full blur-[100px] pointer-events-none opacity-30 mix-blend-screen" />

                <main className="flex-1 overflow-y-auto relative z-10 scroll-smooth pt-16 md:pt-0">
                    <div className="max-w-7xl mx-auto p-4 md:p-8 lg:p-10 space-y-6 md:space-y-8 pb-32">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};
