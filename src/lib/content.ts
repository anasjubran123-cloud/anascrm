// Group-level content used across the site. This is the single source of
// truth for the mother site's high-level capability and sector lists, plus
// stub records for the projects parent and the careers parent.
//
// IMPORTANT: per the master prompt's content-truthfulness rule, nothing here
// makes verifiable claims about specific clients, project values, ISO
// numbers, certifications, or partner tiers. Every entry below is either:
//   • a CT capability domain that is publicly known to be in scope, or
//   • a sector CT services, or
//   • a clearly-marked placeholder ({{TODO}}) with `placeholder: true`.
//
// Phase 5 migrates this data into MDX collections under src/content/. Until
// then, Phase 4 pages render straight from these typed records.

import type { Locale } from '@config/site';

export interface BilingualString {
  en: string;
  ar: string;
}

export interface Capability {
  id: string;
  iconName:
    | 'server'
    | 'zap'
    | 'monitor'
    | 'shield'
    | 'pin'
    | 'check';
  title: BilingualString;
  summary: BilingualString;
}

export const groupCapabilities: readonly Capability[] = [
  {
    id: 'data-center-build',
    iconName: 'server',
    title: {
      en: 'Data center design & build',
      ar: 'تصميم وبناء مراكز البيانات',
    },
    summary: {
      en: 'From feasibility through commissioning, including turnkey construction of new and modular data centers.',
      ar: 'من دراسة الجدوى وحتى التشغيل، شاملاً البناء المتكامل لمراكز البيانات الجديدة والوحدات الجاهزة.',
    },
  },
  {
    id: 'critical-power',
    iconName: 'zap',
    title: {
      en: 'Critical power systems',
      ar: 'أنظمة الطاقة الحرجة',
    },
    summary: {
      en: 'UPS, generators, switchgear, PDUs, and the redundancy topologies that keep production running.',
      ar: 'أنظمة الإمداد المتواصل بالطاقة، المولدات، اللوحات، والوحدات الاحتياطية التي تضمن استمرارية التشغيل.',
    },
  },
  {
    id: 'precision-cooling',
    iconName: 'check',
    title: {
      en: 'Precision cooling',
      ar: 'التبريد الدقيق',
    },
    summary: {
      en: 'CRAC, IRCU, and direct-liquid cooling sized to your IT load profile, climate, and redundancy class.',
      ar: 'حلول التبريد الدقيق المصممة وفق حجم الحمل التقني، المناخ، ومستوى التكرار المطلوب.',
    },
  },
  {
    id: 'it-infrastructure',
    iconName: 'monitor',
    title: {
      en: 'IT infrastructure',
      ar: 'البنية التحتية لتقنية المعلومات',
    },
    summary: {
      en: 'Networking, compute, storage, and structured cabling integrated against vendor-neutral architectures.',
      ar: 'حلول الشبكات والحوسبة والتخزين والكابلات المنظمة وفق معماريات محايدة بين المورّدين.',
    },
  },
  {
    id: 'av-control-rooms',
    iconName: 'monitor',
    title: {
      en: 'Audiovisual & control rooms',
      ar: 'الأنظمة السمعبصرية وغرف التحكم',
    },
    summary: {
      en: 'Video walls, conferencing, signal flow, and operations centers for boardrooms and control environments.',
      ar: 'شاشات العرض الجدارية، أنظمة الاجتماعات، تدفّق الإشارة، ومراكز العمليات.',
    },
  },
  {
    id: 'security-low-current',
    iconName: 'shield',
    title: {
      en: 'CCTV, access control, low-current',
      ar: 'الكاميرات وأنظمة الدخول والتيار المنخفض',
    },
    summary: {
      en: 'Physical security and low-current systems integrated with the building and IT environments they protect.',
      ar: 'أنظمة الأمن المادي والتيار المنخفض المتكاملة مع البيئة المعمارية والتقنية.',
    },
  },
  {
    id: 'pre-sales-tendering',
    iconName: 'check',
    title: {
      en: 'Pre-sales engineering & tendering',
      ar: 'الهندسة قبل البيع وإعداد العطاءات',
    },
    summary: {
      en: 'BoQs, technical compliance, vendor coordination, and proposals built for Saudi tender realities.',
      ar: 'قوائم الكميات، الامتثال الفني، التنسيق مع المورّدين، وإعداد العروض الفنية والمالية.',
    },
  },
  {
    id: 'commissioning-om',
    iconName: 'check',
    title: {
      en: 'Testing, commissioning & O&M',
      ar: 'الاختبار والتشغيل والصيانة',
    },
    summary: {
      en: 'IST, integrated systems testing, and ongoing operations and maintenance contracts at agreed SLAs.',
      ar: 'اختبارات الأنظمة المتكاملة، التشغيل، وعقود الصيانة بمستويات خدمة متفق عليها.',
    },
  },
];

export interface Sector {
  id: string;
  title: BilingualString;
  blurb: BilingualString;
}

export const sectors: readonly Sector[] = [
  {
    id: 'government',
    title: { en: 'Government', ar: 'القطاع الحكومي' },
    blurb: {
      en: 'Ministries, semi-government entities, and Vision 2030 programs.',
      ar: 'الوزارات والجهات شبه الحكومية وبرامج رؤية 2030.',
    },
  },
  {
    id: 'banking',
    title: { en: 'Banking & finance', ar: 'القطاع المصرفي والمالي' },
    blurb: {
      en: 'Banks, fintech, payment processors, and capital-markets infrastructure.',
      ar: 'البنوك والتقنية المالية وبنية تحتية لأسواق المال.',
    },
  },
  {
    id: 'telecom',
    title: { en: 'Telecom', ar: 'الاتصالات' },
    blurb: {
      en: 'MNOs, ISPs, and carrier-grade environments.',
      ar: 'مشغلو الشبكات ومزودو الخدمة والبيئات على مستوى الناقل.',
    },
  },
  {
    id: 'oil-gas',
    title: { en: 'Oil & gas', ar: 'النفط والغاز' },
    blurb: {
      en: 'Upstream, downstream, and corporate facilities for energy operators.',
      ar: 'الأعمال العليا والسفلى والمنشآت المؤسسية لشركات الطاقة.',
    },
  },
  {
    id: 'healthcare',
    title: { en: 'Healthcare', ar: 'الرعاية الصحية' },
    blurb: {
      en: 'Hospitals, healthcare networks, and clinical IT environments.',
      ar: 'المستشفيات والشبكات الصحية والبيئات الإكلينيكية.',
    },
  },
  {
    id: 'education',
    title: { en: 'Education & research', ar: 'التعليم والبحث' },
    blurb: {
      en: 'Universities, research centers, and large-campus environments.',
      ar: 'الجامعات ومراكز الأبحاث والحرم الجامعي الكبير.',
    },
  },
  {
    id: 'enterprise',
    title: { en: 'Enterprise', ar: 'المؤسسات' },
    blurb: {
      en: 'Conglomerates and industrial operators with on-prem and hybrid estates.',
      ar: 'الشركات الكبرى والمشغلون الصناعيون ببنى داخلية وهجينة.',
    },
  },
  {
    id: 'dc-operators',
    title: { en: 'DC owners & operators', ar: 'مالكو ومشغلو مراكز البيانات' },
    blurb: {
      en: 'Co-location, hyperscale, and modular DC operators across the Kingdom.',
      ar: 'مشغلو الإيواء وفائقي الحجم والمراكز المتنقلة في المملكة.',
    },
  },
];

export interface PlaceholderProject {
  id: string;
  sector: string;
  title: BilingualString;
  excerpt: BilingualString;
  approved: boolean;
  placeholder: true;
}

// All projects ship as placeholders until CT confirms disclosure approval per
// case study (Mawani / KFUPM / TRSDC etc.).
export const placeholderProjects: readonly PlaceholderProject[] = [
  {
    id: 'placeholder-dc-1',
    sector: 'banking',
    title: {
      en: '{{TODO: Bank tier-III data center}}',
      ar: '{{TODO: مركز بيانات بنك من المستوى الثالث}}',
    },
    excerpt: {
      en: 'Placeholder case study — full content lands once written client approval is on file.',
      ar: 'دراسة حالة مؤقتة — تنشر التفاصيل عند توفر موافقة العميل الخطية.',
    },
    approved: false,
    placeholder: true,
  },
  {
    id: 'placeholder-government',
    sector: 'government',
    title: {
      en: '{{TODO: Government data center upgrade}}',
      ar: '{{TODO: تحديث مركز بيانات حكومي}}',
    },
    excerpt: {
      en: 'Placeholder case study — content held back pending disclosure approval.',
      ar: 'دراسة حالة مؤقتة — يحتفظ بالمحتوى لحين الحصول على موافقة الإفصاح.',
    },
    approved: false,
    placeholder: true,
  },
  {
    id: 'placeholder-edu',
    sector: 'education',
    title: {
      en: '{{TODO: Research university campus build}}',
      ar: '{{TODO: مشروع حرم جامعة بحثية}}',
    },
    excerpt: {
      en: 'Placeholder case study — content held back pending disclosure approval.',
      ar: 'دراسة حالة مؤقتة — يحتفظ بالمحتوى لحين الحصول على موافقة الإفصاح.',
    },
    approved: false,
    placeholder: true,
  },
];

export interface PartnerStub {
  id: string;
  name: string;
  approved: boolean;
}

// Partner names without tier claims. Per master prompt: include logos when
// the user pushes binaries, but no tier wording until written approval.
export const partners: readonly PartnerStub[] = [
  { id: 'schneider', name: 'Schneider Electric', approved: false },
  { id: 'vertiv', name: 'Vertiv', approved: false },
  { id: 'huawei', name: 'Huawei', approved: false },
  { id: 'stulz', name: 'Stulz', approved: false },
  { id: 'grc', name: 'GRC', approved: false },
  { id: 'tatco', name: 'Tatco', approved: false },
];

export interface SampleRole {
  id: string;
  title: BilingualString;
  location: BilingualString;
  type: 'full-time' | 'part-time' | 'contract' | 'internship';
  summary: BilingualString;
}

export const sampleRoles: readonly SampleRole[] = [
  {
    id: 'placeholder-pm',
    title: {
      en: '{{TODO: Senior Project Manager — Data Centers}}',
      ar: '{{TODO: مدير مشاريع أول — مراكز البيانات}}',
    },
    location: { en: 'Al Khobar, Saudi Arabia', ar: 'الخبر، المملكة العربية السعودية' },
    type: 'full-time',
    summary: {
      en: 'Placeholder role — replace with the live JD before launch.',
      ar: 'وظيفة مؤقتة — تستبدل بالوصف الوظيفي الفعلي قبل النشر.',
    },
  },
];

export interface SampleArticle {
  id: string;
  publishedAt: string;
  title: BilingualString;
  excerpt: BilingualString;
}

export const sampleArticles: readonly SampleArticle[] = [
  {
    id: 'sample-launch',
    publishedAt: '2026-05-08',
    title: {
      en: 'Convergent launches its new corporate site',
      ar: 'كونفرجنت تطلق موقعها المؤسسي الجديد',
    },
    excerpt: {
      en: 'A note on the brand refresh and what to expect from this site over the coming quarters.',
      ar: 'ملاحظة عن تجديد الهوية وما يمكن توقعه من الموقع خلال الأرباع القادمة.',
    },
  },
];

// Helper to read the right language from any bilingual record.
export function pick<T extends BilingualString>(record: T, locale: Locale): string {
  return record[locale];
}
