import gridlines from "../assets/grid-layer.png";

function App() {
  return (
    <div
      style={{
        backgroundImage: `url(${gridlines})`,
      }}
      className="w-screen h-screen bg-no-repeat bg-cover bg-center flex justify-center text-center bg-[#E2E1EC]"
    >
      <div className="flex flex-col justify-center text-primary">
        <h1 className="text-4xl font-bold">Welcome to HayaNG</h1>
        <p className="text-lg mt-4">Fawaz never give us landing page😂😂😂</p>

        <a href="/searchengine">
          <button className="mt-4 px-4 py-2 bg-secondary text-white rounded-md">
            Go to searchengine
          </button>
        </a>
      </div>
    </div>
  );
}

export default App;
