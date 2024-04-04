import useStore from "../store";

function ModalLayout() {
  const { currentModal, setModal } = useStore();

  return (
    <div
      onClick={() => setModal(null)}
      className="fixed top-0 left-0 w-screen h-screen bg-[black]/[.5] z-[101]
    justify-center items-center flex overflow-x-hidden overflow-y-auto
    inset-0 outline-none focus:outline-none p-4 md:p-8"
    >
      {currentModal}
    </div>
  );
}

export default ModalLayout;
