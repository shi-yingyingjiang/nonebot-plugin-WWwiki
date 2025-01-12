# coding=utf-8
from typing import Optional
from pydantic import BaseModel, Field


class Child1(BaseModel):
    id: int
    key: None
    name: str
    parent_id: None = Field(..., alias='parentId')
    level: int
    sort: None
    children: None


class Child(BaseModel):
    id: int
    key: None
    name: str
    parent_id: None = Field(..., alias='parentId')
    level: int
    sort: None
    children: list[Child1]


class OrgTree(BaseModel):
    id: int
    key: None
    name: str
    parent_id: None = Field(..., alias='parentId')
    level: int
    sort: None
    children: list[Child]


class InfoItem(BaseModel):
    text: str


class Figure(BaseModel):
    url: str
    name: str
    real_file_name: str = Field(..., alias='realFileName')
    vertical_figure_url: Optional[str] = Field(None, alias='verticalFigureUrl')
    vertical_figure_real_file_name: Optional[str] = Field(None, alias='verticalFigureRealFileName')


class Role(BaseModel):
    info: list[InfoItem]
    title: str
    figures: list[Figure]
    camp_icon: str = Field(..., alias='campIcon')
    subtitle: str
    role_description: str = Field(..., alias='roleDescription')
    role_description_title: str = Field(..., alias='roleDescriptionTitle')


class TitleStyle(BaseModel):
    color: str
    opacity: str
    text_align: str = Field(..., alias='textAlign')
    background_color: str = Field(..., alias='backgroundColor')
    background_image: str = Field(..., alias='backgroundImage')
    background_position_x: str = Field(..., alias='backgroundPositionX')
    background_position_y: str = Field(..., alias='backgroundPositionY')
    background_image_width: int = Field(..., alias='backgroundImageWidth')
    background_image_height: int = Field(..., alias='backgroundImageHeight')


class MainStyle(BaseModel):
    background_color: str = Field(..., alias='backgroundColor')


class Tab(BaseModel):
    title: str
    active: bool
    content: str


class Component(BaseModel):
    role: Optional[Role] = None
    size: str
    type: str
    title: str
    content: str
    collapse: bool
    title_style: TitleStyle = Field(..., alias='titleStyle')
    main_style: Optional[MainStyle] = Field(None, alias='mainStyle')
    tabs: Optional[list[Tab]] = None
    float: Optional[str] = None
    tabs_type: Optional[str] = Field(None, alias='tabsType')


class Module(BaseModel):
    title: str
    components: list[Component]
    title_disabled: bool = Field(..., alias='titleDisabled')


class Content(BaseModel):
    title: str
    modules: list[Module]


class UserScoreListItem(BaseModel):
    user_id: int = Field(..., alias='userId')
    user_name: str = Field(..., alias='userName')
    head_code: str = Field(..., alias='headCode')
    # is_official: int = Field(..., alias='isOfficial')
    # mobile: str
    user_head_url: str = Field(..., alias='userHeadUrl')
    # identification_type: int | None = Field(..., alias='identificationType')
    status: int
    user_center_url: str = Field(..., alias='userCenterUrl')
    # follow: None
    # puid: str


class Data(BaseModel):
    id: str
    name: str
    org_full_name: str = Field(..., alias='orgFullName')
    org_tree: OrgTree = Field(..., alias='orgTree')
    org_id: int = Field(..., alias='orgId')
    org_id_list: list[int] = Field(..., alias='orgIdList')
    content: Content
    current_version: str = Field(..., alias='currentVersion')
    online_version: str = Field(..., alias='onlineVersion')
    browse_count: int = Field(..., alias='browseCount')
    last_update_time: str = Field(..., alias='lastUpdateTime')
    last_edit_user_name: str = Field(..., alias='lastEditUserName')
    user_score_list: list[UserScoreListItem] = Field(..., alias='userScoreList')
    status: int
    check_status: int = Field(..., alias='checkStatus')


class Model(BaseModel):
    code: int
    msg: str
    data: Data
