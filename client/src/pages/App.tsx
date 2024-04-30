import About from "../components/HomePage/About";
import Faq from "../components/HomePage/Faq";
import Footer from "../components/HomePage/Footer";
import Hero from "../components/HomePage/Hero";
import HowItWorks from "../components/HomePage/HowItWorks";
import Navbar from "../components/HomePage/Navbar";

function App() {
  return (
    <div className="bg-[#FBF8FF] h-screen">
      <Navbar />
      <Hero />
      <About />
      <HowItWorks />
      <Faq />
      <Footer />
    </div>
  );
}

export default App;
