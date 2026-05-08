import type { Locale } from './site';

// Single source of truth for the four business-unit subsidiaries linked from
// the mother site. Updating a destination URL or label happens here only.
//
// IA decision (session 2026-05-08):
//   - Mother site at www.convergent.sa renders link-out cards for each unit.
//   - Each unit lives on its own subdomain and is built separately.
//   - URLs are placeholders until each subsite is provisioned; they remain in
//     this file for grep-ability and so the launch checklist can verify them.

export type BusinessUnitId = 'av' | 'it' | 'dc' | 'landscaping';

export interface BusinessUnit {
  id: BusinessUnitId;
  url: string;
  // Display labels per locale.
  label: Record<Locale, string>;
  // One-line teaser per locale; full copy lives in src/content/business-units/.
  teaser: Record<Locale, string>;
}

export const businessUnits: readonly BusinessUnit[] = [
  {
    id: 'dc',
    url: 'https://dc.convergent.sa',
    label: {
      en: 'Convergent Data Centers',
      ar: 'كونفرجنت لمراكز البيانات',
    },
    teaser: {
      en: 'Design, build, and operate enterprise and turnkey data centers across the Kingdom.',
      ar: 'تصميم وبناء وتشغيل مراكز البيانات للمؤسسات والمشاريع المتكاملة في المملكة.',
    },
  },
  {
    id: 'it',
    url: 'https://it.convergent.sa',
    label: {
      en: 'Convergent IT Infrastructure',
      ar: 'كونفرجنت للبنية التحتية لتقنية المعلومات',
    },
    teaser: {
      en: 'Networking, compute, storage, and structured cabling for mission-critical environments.',
      ar: 'حلول الشبكات والحوسبة والتخزين والكابلات المنظمة للبيئات الحرجة.',
    },
  },
  {
    id: 'av',
    url: 'https://av.convergent.sa',
    label: {
      en: 'Convergent Audiovisual',
      ar: 'كونفرجنت للأنظمة السمعبصرية',
    },
    teaser: {
      en: 'Video walls, control rooms, corporate AV, and conferencing for boardroom and operations.',
      ar: 'شاشات العرض الجداريّة وغرف التحكم وأنظمة الاجتماعات للمؤسسات.',
    },
  },
  {
    id: 'landscaping',
    url: 'https://landscaping.convergent.sa',
    label: {
      en: 'Convergent Landscape',
      ar: 'كونفرجنت لأعمال البيئة المعمارية',
    },
    teaser: {
      en: 'Landscape architecture and outdoor environments tied to corporate facilities.',
      ar: 'تنسيق المواقع والبيئات الخارجية للمنشآت المؤسسية.',
    },
  },
] as const;
