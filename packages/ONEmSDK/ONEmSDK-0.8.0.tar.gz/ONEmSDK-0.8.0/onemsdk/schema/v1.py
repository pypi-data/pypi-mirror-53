from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel, Schema

from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import (FormTag, SectionTag, LiTag, PTag, BrTag, UlTag,
                            ATag, HeaderTag, FooterTag, InputTag)
from onemsdk.parser.tag import InputTagType


class MenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class HttpMethod(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'


class MenuItem(BaseModel):
    """
    [`Menu`](#menu) related component used to display menu items, selectable or
    raw
    """
    type: MenuItemType = Schema(
        ...,
        description='Indicates the type of the object'
    )
    description: str = Schema(
        ...,
        description='The displayed text for this `MenuItem`'
    )
    text_search: str = Schema(
        None,
        description='If the user does not send a proper option marker and '
                    'sends some input, this field will be used to search and '
                    'narrow down the options against the user input. <br> max'
                    ' 1000 chars'
    )
    method: HttpMethod = Schema(
        None,
        description='HTTP method indicating how to trigger the callback path. '
                    'Defaults to `"GET"`'
    )
    path: str = Schema(
        None,
        description='Next route callback path, accessed upon user selection '
                    '<br> _required only for `type=option`_'
    )

    def __init__(self, description: str, text_search: str = None,
                 method: HttpMethod = None, path: str = None):
        if path:
            type_ = MenuItemType.option
            method = method or HttpMethod.GET
        else:
            type_ = MenuItemType.content
        super(MenuItem, self).__init__(type=type_, description=description,
                                       text_search=text_search, method=method, path=path)

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]) -> Optional['MenuItem']:
        if isinstance(tag, str):
            description = tag
        else:
            description = tag.render()

        if not description:
            return None

        method = None
        path = None
        text_search = None

        if isinstance(tag, LiTag):
            child = tag.children[0]
            if isinstance(child, ATag):
                method = child.attrs.method
                path = child.attrs.href
                text_search = tag.attrs.text_search

        return MenuItem(description=description, text_search=text_search, method=method,
                        path=path)


MenuItem.update_forward_refs()


class MenuMeta(BaseModel):
    """
   [`Menu`](#menu) related component holding configuration fields for the menu
    """
    auto_select: bool = Schema(
        False,
        description='Will be automatically selected if set to `true` and in '
                    'case of a single option in the menu'
    )


MenuMeta.update_forward_refs()


class Menu(BaseModel):
    """
    A top level component used to display a menu or raw text
    """
    type: str = Schema(
        'menu',
        description='Indicates the type of the object, defaults to `"menu"`',
        const=True
    )
    body: List[MenuItem] = Schema(
        ..., description='Composed of [`MenuItem`](#menuitem) objects')
    header: str = Schema(None, description='The header of the menu')
    footer: str = Schema(None, description='The header of the menu')

    meta: MenuMeta = Schema(
        None,
        description='[`MenuMeta`](#menumeta) object. Contains configuration '
                    'flags'
    )

    def __init__(self, body: List[MenuItem], header: str = None, footer: str = None,
                 meta: MenuMeta = None):
        super(Menu, self).__init__(type='menu', body=body, header=header, footer=footer,
                                   meta=meta)

    @classmethod
    def from_tag(cls, section_tag: SectionTag) -> 'Menu':
        body = []
        header = None
        footer = None

        for child in section_tag.children:
            if isinstance(child, UlTag):
                body.extend([MenuItem.from_tag(li) for li in child.children])
            elif isinstance(child, HeaderTag):
                header = child.render()
            elif isinstance(child, FooterTag):
                footer = child.render()
            else:
                body.append(MenuItem.from_tag(child))

        return Menu(
            body=list(filter(None, body)),
            header=header or section_tag.attrs.header,
            footer=footer or section_tag.attrs.footer,
            meta=MenuMeta(
                auto_select=section_tag.attrs.auto_select
            )
        )


Menu.update_forward_refs()


class FormItemType(str, Enum):
    string = 'string'  # the user should enter a string during this step
    date = 'date'  # the user should enter a date
    datetime = 'datetime'  # the user should enter a date and a time
    hidden = 'hidden'  # will not be displayed to the user
    int = 'int'  # the user should enter an integer
    float = 'float'  # the user could enter a floating number
    form_menu = 'form-menu'  # the user should choose an option from the menu
    email = 'email'  # the user should send a valid email address
    url = 'url'  # the user should send a valid url
    location = 'location'  # the user should send a valid location
    regex_ = 'regex'  # validated against an ECMA script regex pattern


class MenuItemFormItem(BaseModel):
    """
    [`FormItem`](#formitem) related component used to display menu items,
    selectable or raw
    """
    type: MenuItemType = Schema(
        ...,
        description='Indicates the type of the object'
    )
    description: str = Schema(
        ..., description='The description for this `MenuItemFormItem`')
    value: str = Schema(
        None,
        description='The value for this `MenuItemFormItem`, used in form '
                    'serialization <br> _required only for `type=option`_'
    )
    text_search: str = Schema(
        None,
        description='If the user does not send a proper option marker and '
                    'sends some input, this field will be used to search '
                    'and narrow down the options against the user input '
                    '<br> max 1000 chars'
    )

    def __init__(self, description: str, value: str = None, text_search: str = None):
        if value:
            type_ = MenuItemType.option
        else:
            type_ = MenuItemType.content
        super(MenuItemFormItem, self).__init__(
            type=type_, description=description, value=value, text_search=text_search
        )

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]
                 ) -> Union['MenuItemFormItem', None]:
        value = None
        text_search = None

        if isinstance(tag, str):
            description = tag
        else:
            description = tag.render()

        if not description:
            return None

        if isinstance(tag, LiTag):
            value = tag.attrs.value
            text_search = tag.attrs.text_search

        return MenuItemFormItem(value=value, description=description,
                                text_search=text_search)


MenuItemFormItem.update_forward_refs()


class MenuFormItemMeta(BaseModel):
    """
    [`FormItem`](#formitem) related component holding configuration field for
    a menu inside a form item
    """
    auto_select: bool = Schema(
        False,
        description='Will be automatically selected if set to `true` and in '
                    'case of a single option in the menu'
    )
    multi_select: bool = Schema(
        False,
        description='Allows multiple options to be selected'
    )
    numbered: bool = Schema(
        False,
        description='Displays numbers instead of letter option markers'
    )


MenuFormItemMeta.update_forward_refs()


class FormItem(BaseModel):
    """
    [`Form`](#form) related component used to acquire certain information from
    the user
    """
    type: FormItemType = Schema(
        ...,
        description='Indicates the type of the object'
    )
    name: str = Schema(
        ...,
        description='The name of this `FormItem`, used in form serialization'
    )
    description: str = Schema(None, description='The description of this `FormItem`')
    header: str = Schema(None, description='If provided will overwrite the `Form.header`')
    footer: str = Schema(None, description='If provided will overwrite the `Form.footer`')
    body: List['MenuItemFormItem'] = Schema(
        None,
        description='Composed of [`MenuItemFormItem`](#menuitemformitem) '
                    'objects <br> _required only for `type=form-menu`_'
    )
    value: str = Schema(
        None,
        description='Value to pass in the form serialization data '
                    '<br> _applies only for `type=hidden`_'
    )
    chunking_footer: str = Schema(
        None,
        description='Shown in the footer of the sms chunks'
    )
    confirmation_label: str = Schema(
        None,
        description='Shown in the confirmation menu'
    )
    min_length: int = Schema(
        None,
        description='Validates the user input '
                    '<br> _applies only for `type=string`_'
    )
    min_length_error: str = Schema(
        None,
        description='Message to be shown on `min_length` error'
    )
    max_length: int = Schema(
        None,
        description='Validates the user input '
                    '<br> _applies only for `type=string`_'
    )
    max_length_error: str = Schema(
        None,
        description='Message to be shown on `max_length` error'
    )
    min_value: float = Schema(
        None,
        description='Validates the user input '
                    '<br> _applies only for `type=int|float`_'
    )
    min_value_error: str = Schema(
        None,
        description='Message to be shown on `min_value` error'
    )
    max_value: float = Schema(
        None,
        description='Validates the user input '
                    '<br> _applies only for `type=int|float`_'
    )
    max_value_error: str = Schema(
        None,
        description='Message to be shown on `max_value` error'
    )
    meta: 'MenuFormItemMeta' = Schema(
        None,
        description='[`MenuFormItemMeta`](#menuformitemmeta) object '
                    '<br> _applies only for `type=form-menu`_'
    )
    method: HttpMethod = Schema(
        None,
        description='Http method, how the callback url should be triggered'
    )
    required: bool = Schema(
        False,
        description='User can `SKIP` this `FormItem` if set to `false`'
    )
    pattern: str = Schema(
        None,
        description='ECMA Script regex pattern string '
                    '<br> _applies only for `type=regex`_'
    )
    status_exclude: bool = Schema(
        False,
        description='If `true` this step will be excluded from the form '
                    'completion status'
    )
    status_prepend: bool = Schema(
        False,
        description='If `true` this step will be prepended to the body of '
                    'the response. Appended otherwise'
    )
    url: str = Schema(
        None,
        description='Callback url triggered right after the choice has been '
                    'set for this form item'
    )
    validate_type_error: str = Schema(
        None,
        description='An error message to be shown on basic type validation'
    )
    validate_type_error_footer: str = Schema(
        None,
        description='Shown in the error message footer'
    )
    validate_url: str = Schema(
        None,
        description='The callback url path `"GET"` triggered to validate user input. '
                    '<br> A query string is sent by ONEm: `?form_item_name=user_input` '
                    '<br> The validate_url must return a json response: '
                    '`{"valid": true/false, "error": "Some message in case of '
                    'validation errors"}`'
    )

    def __init__(self, **data):
        super(FormItem, self).__init__(**data)
        if self.body is not None:
            if self.type != FormItemType.form_menu:
                raise ONEmSDKException(
                    f'When "body" param is filled, the type of the '
                    f'FormItem must be {FormItemType.form_menu}.'
                )
        if self.body is None:
            if self.type == FormItemType.form_menu:
                raise ONEmSDKException(
                    f'When type of FormItem is {FormItemType.form_menu}, '
                    f'"body" param must be filled.'
                )
        if self.pattern is not None:
            if self.type != FormItemType.regex_:
                raise ONEmSDKException(
                    f'When "pattern" param is filled, the type of the '
                    f'FormItem must be {FormItemType.regex_}.'
                )
        if self.pattern is None:
            if self.type == FormItemType.regex_:
                raise ONEmSDKException(
                    f'When type of FormItem is {FormItemType.regex_}, '
                    f'"pattern" param must be filled.'
                )

    @classmethod
    def from_tag(cls, section: SectionTag) -> 'FormItem':
        type_ = None
        header = None
        footer = None
        body = []
        value = None
        min_value = None
        min_value_error = None
        min_length = None
        min_length_error = None
        max_value = None
        max_value_error = None
        max_length = None
        max_length_error = None
        description = None
        pattern = None

        content_types_map = {
            InputTagType.date: FormItemType.date,
            InputTagType.datetime: FormItemType.datetime,
            InputTagType.text: FormItemType.string,
            InputTagType.hidden: FormItemType.hidden,
            InputTagType.email: FormItemType.email,
            InputTagType.location: FormItemType.location,
            InputTagType.url: FormItemType.url,
        }

        for child in section.children:
            if isinstance(child, InputTag):
                input_type = child.attrs.type

                # HTML does not have type "int" or "float", it has "number"
                # If the input type is "number", determine if it's "int" or "float"
                if input_type == InputTagType.number:
                    if child.attrs.step == 1:
                        type_ = FormItemType.int
                    else:
                        type_ = FormItemType.float
                elif input_type == InputTagType.hidden:
                    value = child.attrs.value
                    if value is None:
                        raise ONEmSDKException(
                            'value attribute is required for input type="hidden"'
                        )

                is_regex_type = child.attrs.pattern is not None
                if is_regex_type:
                    # Override type with 'regex' if pattern is declared
                    type_ = FormItemType.regex_

                if type_ is None:
                    type_ = content_types_map[input_type]

                min_value = child.attrs.min
                min_value_error = child.attrs.min_error
                min_length = child.attrs.minlength
                min_length_error = child.attrs.minlength_error
                max_value = child.attrs.max
                max_value_error = child.attrs.max_error
                max_length = child.attrs.maxlength
                max_length_error = child.attrs.maxlength_error
                description = section.render(True, True)
                pattern = child.attrs.pattern

                # Ignore other <input> tags if exist
                break
            if isinstance(child, UlTag):
                type_ = FormItemType.form_menu

                for child2 in section.children:
                    if isinstance(child2, UlTag):
                        for li in child.children:
                            menu_item_form_item = MenuItemFormItem.from_tag(li)
                            if menu_item_form_item:
                                body.append(menu_item_form_item)
                    elif isinstance(child2, HeaderTag):
                        pass
                    elif isinstance(child2, FooterTag):
                        pass
                    else:
                        menu_item_form_item = MenuItemFormItem.from_tag(child2)
                        if menu_item_form_item:
                            body.append(menu_item_form_item)
                break
        else:
            raise ONEmSDKException(
                'When <section> plays the role of a form item, '
                'it must contain a <input/> or <ul></ul>'
            )

        if isinstance(section.children[0], HeaderTag):
            header = section.children[0].render()
        if isinstance(section.children[-1], FooterTag):
            footer = section.children[-1].render()

        return FormItem(
            type=type_,
            name=section.attrs.name,
            description=description,
            header=header or section.attrs.header,
            footer=footer or section.attrs.footer,
            body=body or None,
            value=value,
            chunking_footer=section.attrs.chunking_footer,
            confirmation_label=section.attrs.confirmation_label,
            min_value=min_value,
            min_value_error=min_value_error,
            min_length=min_length,
            min_length_error=min_length_error,
            max_value=max_value,
            max_value_error=max_value_error,
            max_length=max_length,
            max_length_error=max_length_error,
            meta=MenuFormItemMeta(
                auto_select=section.attrs.auto_select,
                multi_select=section.attrs.multi_select,
                numbered=section.attrs.numbered,
            ),
            method=section.attrs.method,
            required=section.attrs.required,
            pattern=pattern,
            status_exclude=section.attrs.status_exclude,
            status_prepend=section.attrs.status_prepend,
            url=section.attrs.url,
            validate_type_error=section.attrs.validate_type_error,
            validate_type_error_footer=section.attrs.validate_type_error_footer,
            validate_url=section.attrs.validate_url,
        )


FormItem.update_forward_refs()


class FormMeta(BaseModel):
    """
    [`Form`](#form) related component holding configuration fields for the form
    """
    completion_status_show: bool = Schema(
        False,
        title='Show completion status',
        description='If `true` will show a completion status. Defaults to `false`'
    )
    completion_status_in_header: bool = Schema(
        False,
        title='Show completion status in header',
        description='If `true` will indicate the status in the header. '
                    'Defaults to `false`, which means it will be shown below '
                    'header if the completion status is shown'
    )
    skip_confirmation: bool = Schema(
        False,
        title='Skip confirmation',
        description='If `true` will not ask for confirmation. Defaults to `false`'
    )


FormMeta.update_forward_refs()


class Form(BaseModel):
    """
    A top level component used to acquire information from the user
    """
    type: str = Schema('form',
                       description='Indicates the type of the object, defaults '
                                   'to `"form"`',
                       const=True)
    body: List[FormItem] = Schema(
        ...,
        description='Sequence of [`FormItem`](#formitem) objects used to acquire '
                    'information from user'
    )
    method: HttpMethod = Schema(
        HttpMethod.POST,
        description='HTTP method indicating how to trigger the callback path. '
                    'Defaults to `"POST"`'
    )
    path: str = Schema(
        ...,
        description='The callback path used to send the serialized form data'
    )
    header: str = Schema(
        None,
        description='The header of the form. It can be overwritten by each body component'
    )
    footer: str = Schema(
        None,
        description='The footer of the form. It can be overwritten by each body component'
    )
    meta: FormMeta = Schema(
        None,
        description='[`FormMeta`](#formmeta) object. Contains configuration flags'
    )

    @classmethod
    def from_tag(cls, form_tag: FormTag) -> 'Form':
        body = []
        for section in form_tag.children:
            body.append(FormItem.from_tag(section))

        form = Form(
            header=form_tag.attrs.header,
            footer=form_tag.attrs.footer,
            meta=FormMeta(
                completion_status_show=form_tag.attrs.completion_status_show,
                completion_status_in_header=form_tag.attrs.completion_status_in_header,
                skip_confirmation=form_tag.attrs.skip_confirmation
            ),
            method=form_tag.attrs.method,
            path=form_tag.attrs.action,
            body=body
        )
        return form


Form.update_forward_refs()


class MessageContentType(str, Enum):
    form = 'form'
    menu = 'menu'


class Response(BaseModel):
    """
    Root component wrapping a `Menu` or a `Form`
    """
    content_type: MessageContentType = Schema(
        ...,
        title='Content type',
        description='The content type of the response'
    )
    content: Union[Form, Menu] = Schema(
        ...,
        description='The content of the response. Either `Form` or a `Menu`'
    )

    def __init__(self, content: Union[Menu, Form]):
        if isinstance(content, Menu):
            content_type = MessageContentType.menu
        elif isinstance(content, Form):
            content_type = MessageContentType.form
        else:
            raise ONEmSDKException(f'Cannot create response from {type(content)}')

        super(Response, self).__init__(content_type=content_type, content=content)

    @classmethod
    def from_tag(cls, tag: Union[FormTag, SectionTag]):
        if isinstance(tag, FormTag):
            return Response(content=Form.from_tag(tag))
        if isinstance(tag, SectionTag):
            return Response(content=Menu.from_tag(tag))
        raise ONEmSDKException(f'Cannot create response from {tag.Config.tag_name} tag')


Response.update_forward_refs()
