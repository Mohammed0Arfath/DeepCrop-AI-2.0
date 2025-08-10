/**
 * MIT License
 *
 * Centralized required question IDs for each disease.
 * Keep these IDs in sync with Questionnaire/EnhancedQuestionnaire and backend feature mapping.
 */

export const DEADHEART_IDS = [
  'boreholes_plugged_excreta',
  'central_whorl_dry_withered',
  'affected_shoots_come_off_easily',
  'affected_shoots_wilting_drying',
  'caterpillars_destroying_shoots',
  'reduction_millable_canes',
  'bore_holes_base_ground_level',
  'dirty_white_larvae_violet_stripes',
  'central_shoot_comes_out_easily',
  'small_holes_stem_near_ground',
  'crop_early_growth_phase',
  'leaves_drying_tip_margins',
  'plant_yellow_wilted',
  'rotten_central_shoot_foul_odor',
  'rotten_straw_colored_dead_heart'
];

export const TILLER_IDS = [
  'affected_setts_spreading',
  'plants_stunted_slow_growth',
  'honey_dew_sooty_mould',
  'nodal_regions_infested',
  'tillers_white_yellow',
  'high_aphid_population',
  'gaps_early_drying',
  'cane_stunted_reduced_internodes',
  'no_millable_cane_formation',
  'profuse_lateral_buds',
  'woolly_matter_deposition',
  'gradual_yellowing_drying',
  'yellowing_from_tip_margins',
  'profuse_tillering_3_4_months',
  'ratoon_crop_present'
];

/**
 * Get required question IDs for the selected disease.
 * @param {'deadheart'|'tiller'} diseaseType
 * @returns {string[]}
 */
export function getRequiredQuestionIds(diseaseType) {
  return diseaseType === 'tiller' ? TILLER_IDS : DEADHEART_IDS;
}

/**
 * Compute answered count and completeness given answers map.
 * Expects values 'yes' or 'no' (other values are considered unanswered).
 */
export function getCompletionStatus(diseaseType, answers) {
  const ids = getRequiredQuestionIds(diseaseType);
  const answered = ids.filter((id) => answers[id] === 'yes' || answers[id] === 'no');
  return {
    requiredIds: ids,
    answeredCount: answered.length,
    total: ids.length,
    isComplete: answered.length === ids.length
  };
}
