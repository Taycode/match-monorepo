function NotFound() {
  return (
    <div className="relative flex flex-col items-center justify-center h-screen bg-white/50 dark:bg-black overflow-hidden">
      {/* Starry Background Effect */}
      <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] bg-cover bg-center animate-pulse" />

      {/* Moon */}
      <div className="absolute inset-0 w-[500px] h-[500px] bg-primary/70 dark:bg-primary rounded-full blur-3xl animate-pulse opacity-40 top-[20%] left-[10%]">
        <div className="absolute inset-0 bg-white/60 rounded-full blur-3xl animate-pulse opacity-40"></div>
      </div>

      {/* Futuristic Circle Around Moon */}
      <div className="relative mb-8">
        <div className="w-44 h-44 bg-primary/70 dark:bg-primary opacity-40 rounded-full blur-3xl absolute top-[-80px] left-[-80px]"></div>
        <div className="w-48 h-48 rounded-full absolute top-[-100px] left-[-100px] animate-pulse"></div>
      </div>

      {/* Main 404 Text */}
      <h1 className="relative text-5xl md:text-9xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-gray animate-glow">
        404
      </h1>

      {/* Subheading */}
      <p className="relative text-lg md:text-2xl text-black dark:text-white mt-4 text-center px-4 max-w-lg">
        The page you're looking for could not be found. Please check the URL or
        click the button below to return to the home page.
      </p>

      {/* Button to Go Back */}
      <a
        href="/"
        className="relative mt-6 px-6 py-3 text-xl text-black bg-white hover:bg-gray-100 rounded-lg shadow-lg hover:shadow-primary/50 transition-all duration-300 ease-in-out font-medium font-satoshi tracking-wide"
      >
        Return to Home
      </a>
    </div>
  );
}

export default NotFound;
