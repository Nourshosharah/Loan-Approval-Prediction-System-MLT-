import {
  createContext,
  useContext,
  useState,
  type ReactNode,
  type Dispatch,
  type SetStateAction,
} from "react";
import { IntlProvider, type MessageFormatElement } from "react-intl";
import arMessages from "../locales/ar.json";
import enMessages from "../locales/en.json";

type Messages = Record<string, string> | Record<string, MessageFormatElement[]>;

const messages: Record<"ar" | "en", Messages> = {
  ar: arMessages,
  en: enMessages,
};

type Locale = "ar" | "en";

type I18nContextType = {
  locale: Locale;
  setLocale: Dispatch<SetStateAction<Locale>>;
};

const I18nContext = createContext<I18nContextType>({
  locale: "en",
  setLocale: () => {},
});

export function useI18n() {
  return useContext(I18nContext);
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>("en");

  return (
    <I18nContext.Provider value={{ locale, setLocale }}>
      <IntlProvider
        locale={locale}
        messages={messages[locale]}
        defaultLocale="en"
      >
        {children}
      </IntlProvider>
    </I18nContext.Provider>
  );
}
