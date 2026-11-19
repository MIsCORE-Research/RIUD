# R8 source-native time binding

SXS simulation time is preserved as the native dimensionless coordinate. The common-horizon time is read from each resolution metadata.json and used only to report tau=t_native-common_horizon_time. No event-specific affine warp, detector-frame conversion, R40 refit, or GAP/MT forced registration is used. Waveform and horizon rows remain in their source-native representations.
