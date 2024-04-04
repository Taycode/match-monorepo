export const topLeftVariants = {
  hidden: {
    opacity: 0.3,
    y: "40%",
    x: "30%",
  },
  visible: {
    opacity: 1,
    transition: {
      duration: 1,
    },
    y: "0",
    x: "0",
  },
};

export const fade = {
  hidden: {
    opacity: 0,
  },
  visible: {
    transition: {
      duration: 1.5,
    },
    opacity: 1.2,
  },
};
