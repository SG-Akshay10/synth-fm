import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';

export const GradientButton = ({
    children,
    className,
    variant = 'primary',
    loading = false,
    disabled,
    ...props
}) => {
    const variants = {
        primary: "bg-primary hover:bg-primary/90 text-white shadow-[0_0_20px_rgba(98,71,234,0.3)] hover:shadow-[0_0_30px_rgba(98,71,234,0.5)] border border-white/10",
        secondary: "bg-white/5 hover:bg-white/10 text-white border border-white/10 backdrop-blur-sm",
        accent: "bg-accent hover:bg-accent/90 text-background font-semibold shadow-[0_0_20px_rgba(0,255,128,0.3)] hover:shadow-[0_0_30px_rgba(0,255,128,0.5)]",
        danger: "bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20",
        ghost: "bg-transparent hover:bg-white/5 text-gray-400 hover:text-white"
    };

    return (
        <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={disabled || loading}
            className={cn(
                "relative flex items-center justify-center gap-2 rounded-full px-6 py-3 font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed",
                variants[variant],
                className
            )}
            {...props}
        >
            {loading && <Loader2 className="animate-spin" size={18} />}
            {children}
        </motion.button>
    );
};
