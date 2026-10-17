import './globals.css';
import { StoreProvider } from '@/context/StoreContext';
import CartPanel from '@/components/CartPanel';
import WishlistPanel from '@/components/WishlistPanel';
import SearchOverlay from '@/components/SearchOverlay';
import MobileDrawer from '@/components/MobileDrawer';
import ProductModal from '@/components/ProductModal';
import CheckoutModal from '@/components/CheckoutModal';
import OrderTrackingModal from '@/components/OrderTrackingModal';
import ContactModal from '@/components/ContactModal';
import ArticleModal from '@/components/ArticleModal';
import Toast from '@/components/Toast';
import ScrollReveal from '@/components/ScrollReveal';

export const metadata = {
  title: 'AstroVeda — परंपरेतून मार्गदर्शन • श्रद्धेतून समाधान',
  description: 'Authentic Rudraksha, Gemstones, Yantra, Bracelets and Jyotish Consultation. 25+ years experience. Certified, energised and delivered across India.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="mr">
      <body>
        <StoreProvider>
          <div className="bg-fx" />
          <div className="bg-grain" />
          <ScrollReveal />
          {children}
          <CartPanel />
          <WishlistPanel />
          <SearchOverlay />
          <MobileDrawer />
          <ProductModal />
          <CheckoutModal />
          <OrderTrackingModal />
          <ContactModal />
          <ArticleModal />
          <Toast />
        </StoreProvider>
      </body>
    </html>
  );
}
