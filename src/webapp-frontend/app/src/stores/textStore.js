import { defineStore } from 'pinia'

export const useTextStore = defineStore('text', {
  state: () => ({
    sloganMultiLine: 'Innovating Nature-Care<br>with Smart Technology',
    slogan: 'Innovating Nature-Care with Smart Technology',
    applicationName: 'Leaf Link',
    restApiBaseUrl: `${window.location.origin}/api/v1`,
    // restApiBaseUrl: 'http://mip3-cirie1.tail60817a.ts.net/api/v1',
    // restApiBaseUrl: 'http://localhost/api/v1',


    statusEnum: {
      0: 'Active',
      1: 'Archived',
      2: 'Deleted',
    },
    nodeTemplateStatusEnum: {
      0: { name: 'Unused', label: 'Unused', color: 'warning' },
      1: { name: 'In-use', label: 'In Use', color: 'success' },
      2: { name: 'Archived', label: 'Archived', color: 'grey' },
    },
    ProtobufDataTypes: {
      0: 'double',
      1: 'float',
      2: 'int32',
      3: 'int64',
      4: 'uint32',
      5: 'uint64',
      6: 'sint32',
      7: 'sint64',
      8: 'fixed32',
      9: 'fixed64',
      10: 'sfixed32',
      11: 'sfixed64',
      12: 'bool',
      13: 'string',
      14: 'bytes',
    },
    externalResourceProjectEnum: {
      0: 'Website',
      1: 'MS-Teams',
      2: 'Report',
      3: 'Documentation',
      4: 'Misc',
    },
    externalResourceSensorEnum: {
      0: 'Datasheet',
      1: 'Webshop',
      2: 'Misc'
    },
    sensorUnitsEnum: {
      CELSIUS: '°C',
      FAHRENHEIT: '°F',
      KELVIN: 'K',
      PERCENT: '%',
      VOLT: 'V',
      AMPERE: 'A',
      LUX: 'lx',
      PASCAL: 'Pa',
      KILOPASCAL: 'kPa',
      PH: 'pH',
      MG_PER_L: 'mg/L',
      UG_PER_L: 'µg/L',
      MOL_PER_M2_S: 'mol/m²/s',
      WATT_PER_M2: 'W/m²',
      MS_PER_CM: 'mS/cm',
      METER: 'm',
      MILLIMETER: 'mm',
      CM: 'cm',
      GRAM: 'g',
      KG: 'kg',
      LITER: 'L',
      CUBIC_METER: 'm³',
      PARTS_PER_MILLION: 'ppm',
      PARTS_PER_BILLION: 'ppb',
      DEGREE: '°',
      METERS_PER_SECOND: 'm/s',
      HECTOPASCAL: 'hPa'
    },
    icons: {
      'projects': 'mdi-forest-outline',
      'commercialSensors': 'mdi-chip',
      'nodeTemplates': 'mdi-file-document-multiple',
      'sensorNodes': 'mdi-wifi',
    }
  }),
})