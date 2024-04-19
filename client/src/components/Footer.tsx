import global from "../assets/global.svg";
import help from "../assets/messages.svg";
import instagram from "../assets/Instagram.svg";
import twitter from "../assets/twitter.svg";

function Footer() {
  return (
    <div className="flex flex-col md:flex-row max-w-7xl mx-auto justify-between items-center gap-4 p-4 md:p-8">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
          <img src={twitter} alt="twitter" />
          <h6 className="font-medium text-primary font-satoshi">@hayang</h6>
        </div>
        <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
          <img src={instagram} alt="instagram" />
          <h6 className="font-medium text-primary font-satoshi">@hayang</h6>
        </div>
        <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
          <img src={global} alt="instagram" />
          <h6 className="font-medium text-primary font-satoshi">haya.ng</h6>
        </div>
      </div>
      <div className="flex items-center gap-2 bg-[#F1F0FA] p-2.5 rounded-xl">
        <img src={help} alt="instagram" />
        <h6 className="font-medium text-primary font-satoshi">Help</h6>
      </div>
    </div>
  );
}

export default Footer;
