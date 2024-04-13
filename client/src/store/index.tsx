import { create } from "zustand";

const useStore: any = create((set: any) => ({
  currentModal: null,
  setModal: (newModal: any) =>
    set((state: any) => ({ ...state, currentModal: newModal })),
}));

export default useStore;
