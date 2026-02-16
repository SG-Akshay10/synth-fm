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
        primary: "bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white shadow-lg shadow-purple-500/20",
        secondary: "bg-white/10 hover:bg-white/20 text-white border border-white/10 backdrop-blur-sm",
        danger: "bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20",
        ghost: "bg-transparent hover:bg-white/5 text-gray-300 hover:text-white"
    };

    return (
        <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={disabled || loading}
            className={cn(
                "relative flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed",
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
