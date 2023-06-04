import * as migrator from './migrator';
import * as v2 from './v2';
import * as v3 from './v3';
import * as v4 from './v4';
import * as v5 from './v5';
import * as v6 from './v6';
import * as v7 from './v7';
import * as v8 from './v8';
import * as v9 from './v9';
import * as v10 from './v10';
import * as v11 from './v11';

export type {Scale, ScaleType} from './v10';
export type {Signals} from './v11';

export const PLOT_DIMS_UI = v2.PLOT_DIMS_UI;
export const MARK_OPTIONS = v7.MARK_OPTIONS;
export const DEFAULT_POINT_SIZE = v2.DEFAULT_POINT_SIZE;
export const DIM_NAME_MAP = v7.DIM_NAME_MAP;
export const POINT_SHAPES = v6.POINT_SHAPES;
export const LINE_SHAPES = v9.LINE_SHAPE_OPTIONS;
export const SCALE_TYPES = v10.SCALE_TYPES;
export const DEFAULT_SCALE_TYPE = v10.DEFAULT_SCALE_TYPE;

export const {migrate} = migrator
  .makeMigrator(v2.migrate)
  .add(v3.migrate)
  .add(v4.migrate)
  .add(v5.migrate)
  .add(v6.migrate)
  .add(v7.migrate)
  .add(v8.migrate)
  .add(v9.migrate)
  .add(v10.migrate)
  .add(v11.migrate);

export type AnyPlotConfig = Parameters<typeof migrate>[number];
export type PlotConfig = ReturnType<typeof migrate>;

export type SeriesConfig = PlotConfig['series'][number];
export type MarkOption = PlotConfig['series'][number]['constants']['mark'];
export type LineShapeOption =
  PlotConfig['series'][number]['constants']['lineStyle'];
export type AxisSettings = PlotConfig['axisSettings'];
export type Selection = v11.Selection;
export type ContinuousSelection = v11.ContinuousSelection;
export type DiscreteSelection = v11.DiscreteSelection;
export type AxisSelections = v11.AxisSelections;