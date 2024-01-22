import os
import re
import cn2an
import xml.dom.minidom


def format_xml(input_xml):
    dom = xml.dom.minidom.parseString(input_xml)
    formatted_xml = dom.toprettyxml(indent="  ")
    return formatted_xml


def line_process(lines):
    processed_lines = []
    chapter_open = 0
    chapter_close = 0
    section_open = 0
    section_close = 0
    article_open = 0
    article_close = 0
    paragraph_open = 0
    paragraph_close = 0
    paragraph_count = 0

    for line in lines:
        trimmed_line = line.strip(" 　").rstrip("\n")

        if re.match(r"^第[零一二三四五六七八九十]{1,3}章", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1
            if section_open - 1 == section_close:
                processed_lines.append("</Section>")
                section_close += 1
            if chapter_open - 1 == chapter_close:
                processed_lines.append("</Chapter>")
                chapter_close += 1

            chapter_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十]{1,3})章", trimmed_line).group(1)
            )

            processed_lines.append(
                f'<Chapter Num="{chapter_num}"><ChapterTitle>{trimmed_line}</ChapterTitle>'
            )

            chapter_open += 1
            section_open = 0
            section_close = 0

        elif re.match(r"^第[零一二三四五六七八九十]{1,3}节", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1
            if section_open - 1 == section_close:
                processed_lines.append("</Section>")
                section_close += 1

            section_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十]{1,3})节", trimmed_line).group(1)
            )

            processed_lines.append(
                f'<Section Num="{section_num}"><SectionTitle>{trimmed_line}</SectionTitle>'
            )

            section_open += 1

        elif re.match(r"^第[零一二三四五六七八九十百千]{1,7}条[ 　]+", trimmed_line):
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            if article_open - 1 == article_close:
                processed_lines.append("</Article>")
                article_close += 1

            article_title = re.search(r"^(第[零一二三四五六七八九十百千]{1,7}条)", trimmed_line).group(
                1
            )
            first_paragraph_content = re.search(
                r"^第[零一二三四五六七八九十百千]{1,7}条[ 　]+(.*)$", trimmed_line
            ).group(1)
            article_num = cn2an.cn2an(
                re.search(r"^第([零一二三四五六七八九十百千]{1,7})条", trimmed_line).group(1)
            )

            if (
                len(first_paragraph_content.split("。")) > 2
                or len(first_paragraph_content.split("；")) > 2
            ):
                first_paragraph_content_list = re.split(
                    r"(?<=[。；])", first_paragraph_content
                )
                if (
                    first_paragraph_content_list
                    and first_paragraph_content_list[-1] == ""
                ):
                    first_paragraph_content_list.pop()
                sentences = ""
                for index in range(len(first_paragraph_content_list)):
                    if "但" in first_paragraph_content_list[index][0]:
                        sentences += f'<Sentence Num="{index + 1}" Function="proviso">{first_paragraph_content_list[index]}</Sentence>'
                    else:
                        sentences += f'<Sentence Num="{index + 1}">{first_paragraph_content_list[index]}</Sentence>'
                processed_lines.append(
                    f'<Article Num="{article_num}"><ArticleTitle>{article_title}</ArticleTitle><Paragraph Num="1"><ParagraphNum/><ParagraphSentence>{sentences}</ParagraphSentence>'
                )
            else:
                processed_lines.append(
                    f'<Article Num="{article_num}"><ArticleTitle>{article_title}</ArticleTitle><Paragraph Num="1"><ParagraphNum/><ParagraphSentence><Sentence>{first_paragraph_content}</Sentence></ParagraphSentence>'
                )

            article_open += 1
            paragraph_open += 1
            paragraph_count = 1

        elif re.match(r"^[\(（][零一二三四五六七八九十]{1,3}[\)）]", trimmed_line):
            item_title = re.search(
                r"^([\(（][零一二三四五六七八九十]{1,3}[\)）])", trimmed_line
            ).group(1)
            item_content = re.search(
                r"^[\(（][零一二三四五六七八九十]{1,3}[\)）](.*)$", trimmed_line
            ).group(1)
            item_num = cn2an.cn2an(
                re.search(r"^[\(（]([零一二三四五六七八九十]{1,3})[\)）]", trimmed_line).group(1)
            )

            if len(item_content.split("。")) > 2 or len(item_content.split("；")) > 2:
                item_content_list = re.split(r"(?<=[。；])", item_content)
                if item_content_list and item_content_list[-1] == "":
                    item_content_list.pop()
                sentences = ""
                for index in range(len(item_content_list)):
                    if "但" in item_content_list[index][0]:
                        sentences += f'<Sentence Num="{index + 1}" Function="proviso">{item_content_list[index]}</Sentence>'
                    else:
                        sentences += f'<Sentence Num="{index + 1}">{item_content_list[index]}</Sentence>'
                processed_lines.append(
                    f'<Item Num="{item_num}"><ItemTitle>{item_title}</ItemTitle><ItemSentence>{sentences}</ItemSentence></Item>'
                )
            else:
                processed_lines.append(
                    f'<Item Num="{item_num}"><ItemTitle>{item_title}</ItemTitle><ItemSentence><Sentence>{item_content}</Sentence></ItemSentence></Item>'
                )

        else:
            if paragraph_open - 1 == paragraph_close:
                processed_lines.append("</Paragraph>")
                paragraph_close += 1
            paragraph_count += 1

            if len(trimmed_line.split("。")) > 2 or len(trimmed_line.split("；")) > 2:
                trimmed_line_list = re.split(r"(?<=[。；])", trimmed_line)
                if trimmed_line_list and trimmed_line_list[-1] == "":
                    trimmed_line_list.pop()
                sentences = ""
                for index in range(len(trimmed_line_list)):
                    if "但" in trimmed_line_list[index][0]:
                        sentences += f'<Sentence Num="{index + 1}" Function="proviso">{trimmed_line_list[index]}</Sentence>'
                    else:
                        sentences += f'<Sentence Num="{index + 1}">{trimmed_line_list[index]}</Sentence>'
                processed_lines.append(
                    f'<Paragraph Num="{paragraph_count}"><ParagraphNum/><ParagraphSentence>{sentences}</ParagraphSentence>'
                )
            else:
                processed_lines.append(
                    f'<Paragraph Num="{paragraph_count}"><ParagraphNum/><ParagraphSentence><Sentence>{trimmed_line}</Sentence></ParagraphSentence>'
                )

            paragraph_open += 1

    if paragraph_open - 1 == paragraph_close:
        processed_lines.append("</Paragraph>")
    if article_open - 1 == article_close:
        processed_lines.append("</Article>")
    if section_open - 1 == section_close:
        processed_lines.append("</Section>")
    if chapter_open - 1 == chapter_close:
        processed_lines.append("</Chapter>")

    return processed_lines


if __name__ == "__main__":
    input_file_name = input("请指定本目录下要处理的纯文本文件的文件名（推荐格式为“法律名称.txt”）：")
    output_file_name = input_file_name.split(".")[0] + "_formatted.xml"

    input_file_path = os.path.join(os.getcwd(), input_file_name)

    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            lines = [line for line in file.readlines() if line.strip()]

        processed_lines = line_process(lines)

        xml_text = f'<Law><LawBody><MainProvision><LawTitle>{input_file_name.split(".")[0]}</LawTitle>{"".join(processed_lines)}</MainProvision></LawBody></Law>'

        formatted_xml = format_xml(xml_text)

        with open(output_file_name, "w", encoding="utf-8") as file:
            file.write(formatted_xml)

        print(f"处理成功。已输出到同目录下的“{output_file_name}”。")

    except FileNotFoundError:
        print(f"指定的文件不存在，请检查输入。")
    except Exception as e:
        print(f"发生错误: {str(e)}")
